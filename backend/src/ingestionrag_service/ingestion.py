from qdrant_client import QdrantClient
from qdrant_client.models import models, PointStruct
from fastembed import TextEmbedding
from pathlib import Path
from settings import Settings

s = Settings()

# Connect to Qdrant. Ensure s.client points to a local directory or valid host
# Example for local storage in settings.py: client = "./qdrant_database"
client = QdrantClient(s.client)
collection_name = s.collection_name

# Load ONLY the dense embedding model to save memory and compute time
dense_model = TextEmbedding(s.dense_model)

def get_points(directory_path):
    path = Path(directory_path)
    files = [f for f in path.iterdir() if f.is_file()]
    texts = [f.read_text(encoding="utf-8") for f in files]

    # Compute ONLY dense embeddings (much faster)
    dense_vecs = list(dense_model.embed(texts))

    for idx, (file, d) in enumerate(zip(files, dense_vecs)):
        print(f"Embedding: {file.name}")
        yield PointStruct(
            id=idx,
            vector={
                "dense": d.tolist(),
            },
            payload={"title": file.name, "description": texts[idx]}
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
        }
    )

    # 3. Process and upload the documents
    print("Uploading documents...")
    client.upload_points(
        collection_name=collection_name,
        points=get_points(s.docs_path),
        batch_size=1
    )
    print("Upload completed successfully!")