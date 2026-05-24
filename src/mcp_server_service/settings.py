from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    dense_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    sparse_model: str = "prithivida/Splade_PP_en_v1"
    late_model: str = "colbert-ir/colbertv2.0"
    host: str = "0.0.0.0"   
    port: int = 8021             

    mlflow_prompt_name : str = 'rag_prompt'
    mlflow_prompt_alias : str = 'rag'