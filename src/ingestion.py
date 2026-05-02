from dataclasses import dataclass
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, models, Document, PointStruct

client = QdrantClient('http://localhost:6333')

collection_name = 'small_metal_parts'

dense_embedding_model = 'BAAI/bge-m3'
sparse_embedding_model = 'Qdrant/bm25'
late_interaction_embedding_model = "answerdotai/answerai-colbert-small-v1"


if client.collection_exists(collection_name=collection_name):
    client.delete_collection(collection_name=collection_name)

client.create_collection(
    collection_name,
    vectors_config={
        "dense": models.VectorParams(
            size=1024,
            distance=models.Distance.COSINE
        ),
        "multi": models.VectorParams(
            size=96,
            distance=models.Distance.COSINE,
            multivector_config=models.MultiVectorConfig(
                comparator=models.MultiVectorComparator.MAX_SIM
            ),
            hnsw_config=models.HnswConfigDiff(m=0)
        ),
    },
    sparse_vectors_config={
        "sparse":models.SparseVectorParams(modifier=models.Modifier.IDF)
    }
)

