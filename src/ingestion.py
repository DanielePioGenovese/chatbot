from dataclasses import dataclass
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, models, Document, PointStruct
from pathlib import Path
from fastembed import TextEmbedding, SparseTextEmbedding, LateInteractionTextEmbedding

import requests

base_url = "http://localhost:6333"

models_to_setup = [
    {"name": "BAAI/bge-small-en-v1.5", "type": "text"},
    {"name": "Qdrant/bm25", "type": "sparse"},
    {"name": "colbert-ir/colbertv2.0", "type": "text"} 
]

for model in models_to_setup:
    response = requests.post(f"{base_url}/collections/inference/models", json=model)
    print(f"Setup {model['name']}: {response.json()}")

client = QdrantClient('http://localhost:6333')

collection_name = 'small_metal_parts'

dense_embedding_model = 'BAAI/bge-base-en'
sparse_embedding_model = 'Qdrant/bm25'
late_interaction_embedding_model = "colbert-ir/colbertv2.0"

dense_model = TextEmbedding("BAAI/bge-small-en-v1.5")
sparse_model = SparseTextEmbedding("Qdrant/bm25")
multi_model = LateInteractionTextEmbedding("colbert-ir/colbertv2.0")

if client.collection_exists(collection_name=collection_name):
    client.delete_collection(collection_name=collection_name)

client.create_collection(
    collection_name,
    vectors_config={
        "dense": models.VectorParams(
            size=768,
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

def get_points(directory_path):
    path = Path(directory_path)
    
    print(f"Reading: {path.absolute()}")

    for idx, file in enumerate(path.iterdir()):
        if not file.is_file():
            continue
            
        content = file.read_text(encoding="utf-8")

        print("FILE CONTENT:")

        print(content)
        
        yield PointStruct(
            id=idx,
            vector={
                "dense": Document(text=content, model=dense_embedding_model),
                "sparse": Document(text=content, model=sparse_embedding_model),
                "multi": Document(text=content, model=late_interaction_embedding_model),
            },
            payload={
                "title": file.name, 
                "description": content
            }
        )

client.upload_points(
    collection_name=collection_name,
    points=get_points('docs'),
    batch_size=25
)