from pydantic_settings import BaseSettings 

class Settings(BaseSettings):
    client: str = 'http://qdrant:6333'
    collection_name: str = 'small_metal_parts'

    dense_model: str = "BAAI/bge-small-en-v1.5"
    sparse_model: str = "Qdrant/bm25"
    multi_model: str = "colbert-ir/colbertv2.0"

    dense_size: int = 384
    sparse_size: int = 128

    docs_path: str = '/docs'