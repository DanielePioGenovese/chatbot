from dataclasses import dataclass
from qdrant_client import QdrantClient
from pydantic import BaseModel

client = QdrantClient('http://localhost:6333')

collection_name = 'small metal parts'

if not client.collection_exists():
    client.create_collection(
        collection_name=collection_name,
        vectors_config=client.get_fastembed_vector_params()
    )

class Documents(BaseModel):
    id : int
    text : str
    metadata : dict

docs = [
    Documents()
]