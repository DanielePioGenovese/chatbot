from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    transport_settings: str = "streamable_http"
    uri_mcp_server : str = "http://mcpserver:8021/mcp"
    uri_mlflow_server : str = "http://mlflow:5000"
    
    # model : str = "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4"
    model : str = 'main_model'
    uri_vllm: str = "http://vllm:8000/v1"
    mflow_prompt_name : str = "main_prompt"
    mflow_prompt_alias: str = "production"

    temperature : float = 0.0
    timeout : int = 120
    
    origins: list[str] = [
    "http://localhost:5500",
    "http://127.0.0.1:5500"
    ]
    
    streaming : bool = True