from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    dense_model: str = "Qdrant/bm42-all-minilm-l6-v2-attentions"
    sparse_model: str = "prithivida/Splade_PP_en_v1"
    late_model: str = "colbert-ir/colbertv2.0"
    host: str = "0.0.0.0"   
    port: int = 6000             