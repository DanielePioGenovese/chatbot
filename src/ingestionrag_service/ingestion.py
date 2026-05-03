from qdrant_client import QdrantClient
from qdrant_client.models import models, PointStruct, SparseVector
from fastembed import TextEmbedding, SparseTextEmbedding, LateInteractionTextEmbedding
from pathlib import Path

client = QdrantClient('http://qdrant:6333')
collection_name = 'small_metal_parts'

# Load models
dense_model  = TextEmbedding("BAAI/bge-small-en-v1.5")
sparse_model = SparseTextEmbedding("Qdrant/bm25")
multi_model  = LateInteractionTextEmbedding("colbert-ir/colbertv2.0")

if client.collection_exists(collection_name=collection_name):
    client.delete_collection(collection_name=collection_name)

client.create_collection(
    collection_name,
    vectors_config={
        "dense": models.VectorParams(size=384, distance=models.Distance.COSINE),
        "multi": models.VectorParams(
            size=128,
            distance=models.Distance.COSINE,
            multivector_config=models.MultiVectorConfig(
                comparator=models.MultiVectorComparator.MAX_SIM
            ),
            hnsw_config=models.HnswConfigDiff(m=0)
        ),
    },
    sparse_vectors_config={
        "sparse": models.SparseVectorParams(modifier=models.Modifier.IDF)
    }
)

def get_points(directory_path):
    path = Path(directory_path)
    files = [f for f in path.iterdir() if f.is_file()]
    texts = [f.read_text(encoding="utf-8") for f in files]

    dense_vecs  = list(dense_model.embed(texts))
    sparse_vecs = list(sparse_model.embed(texts))
    multi_vecs  = list(multi_model.embed(texts))

    for idx, (file, d, s, m) in enumerate(zip(files, dense_vecs, sparse_vecs, multi_vecs)):
        print(f"Embedding: {file.name}")
        yield PointStruct(
            id=idx,
            vector={
                "dense":  d.tolist(),
                "sparse": SparseVector(indices=s.indices.tolist(), values=s.values.tolist()),
                "multi":  m.tolist(),
            },
            payload={"title": file.name, "description": texts[idx]}
        )

client.upload_points(
    collection_name=collection_name,
    points=get_points('docs'),
    batch_size=1
)