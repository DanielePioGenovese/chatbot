from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, models, Document, PointStruct
from pathlib import Path

client = QdrantClient('http://localhost:6333')
collection_name = 'small_metal_parts'

DENSE_MODEL = "BAAI/bge-small-en-v1.5"
SPARSE_MODEL = "Qdrant/bm25"
MULTI_MODEL  = "colbert-ir/colbertv2.0"

if client.collection_exists(collection_name=collection_name):
    client.delete_collection(collection_name=collection_name)

client.create_collection(
    collection_name,
    vectors_config={
        "dense": models.VectorParams(
            size=384,
            distance=models.Distance.COSINE
        ),
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
    print(f"Reading: {path.absolute()}")
    for idx, file in enumerate(path.iterdir()):
        if not file.is_file():
            continue
        content = file.read_text(encoding="utf-8")
        print(f"FILE: {file.name}\n{content}")
        yield PointStruct(
            id=idx,
            vector={
                "dense":  Document(text=content, model=DENSE_MODEL),
                "sparse": Document(text=content, model=SPARSE_MODEL),
                "multi":  Document(text=content, model=MULTI_MODEL),
            },
            payload={"title": file.name, "description": content}
        )

client.upload_points(
    collection_name=collection_name,
    points=get_points('docs'),
    batch_size=1
)