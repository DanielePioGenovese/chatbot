from qdrant_client import QdrantClient
from qdrant_client.models import models, PointStruct
from fastembed import TextEmbedding, SparseTextEmbedding
from pathlib import Path
from settings import Settings

s = Settings()

# Connect to Qdrant. Ensure s.client points to a local directory or valid host
# Example for local storage in settings.py: client = "./qdrant_database"
client = QdrantClient(s.client)
collection_name = s.collection_name

# Load ONLY the dense embedding model to save memory and compute time
def get_points(directory_path):
    path = Path(directory_path)
    files = [f for f in path.iterdir() if f.is_file()]

    def text_generator():
        for f in files:
            yield f.read_text(encoding="utf-8")

    dense_model = TextEmbedding(s.dense_model)
    sparse_model = SparseTextEmbedding(s.sparse_model)

    dense_vecs = dense_model.embed(text_generator())
    sparse_vecs = sparse_model.embed(text_generator())

    for idx, (file, d, sp) in enumerate(zip(files, dense_vecs, sparse_vecs)):
        print(f"Embedding: {file.name}")
        
        text_content = file.read_text(encoding="utf-8") 
        
        yield PointStruct(
            id=idx,
            vector={
                "dense": d.tolist(),
                "sparse": models.SparseVector(
                    indices=sp.indices.tolist(),
                    values=sp.values.tolist()
                )
            },
            payload={"title": file.name, "description": text_content}
        )

# PROTECTION BLOCK: This code executes ONLY when you run this file directly.
# It prevents accidental data deletion if the file is imported elsewhere.
if __name__ == "__main__":
    print(f"Starting process for collection: {collection_name}")
    
    # 1. Reset collection if it exists (Run this ONLY when you need to refresh documents!)
    if client.collection_exists(collection_name=collection_name):
        print("Existing collection found. Deleting it...")
        client.delete_collection(collection_name=collection_name)

    # 2. Create a clean collection with dense vector configuration
    print("Creating new collection...")
    client.create_collection(
        collection_name,
        vectors_config={
            "dense": models.VectorParams(size=s.dense_size, distance=models.Distance.COSINE)
        },
        sparse_vectors_config={
            "sparse": models.SparseVectorParams()
        }
    )

    # 3. Process and upload the documents
    print("Uploading documents...")
    client.upload_points(
        collection_name=collection_name,
        points=get_points(s.docs_path),
        batch_size=64
    )
    print("Upload completed successfully!")