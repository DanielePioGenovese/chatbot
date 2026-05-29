from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    dense_model: str = "BAAI/bge-small-en-v1.5"
    sparse_model: str = "Qdrant/bm25"
    host: str = "0.0.0.0"   
    port: int = 8021             

    mlflow_prompt_name : str = 'rag_prompt'
    mlflow_prompt_alias : str = 'rag'