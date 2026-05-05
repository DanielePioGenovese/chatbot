from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    transport_settings : str = "http"
    uri_mcp_server : str = "http://mcpserver:6000"
    uri_mflow_server : str = "http://mflow:5000"
    
    model : str = "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4"
    uri_vllm : str = "http://vllm:8080"
    mflow_prompt_name : str = "rag-assistant"

    temperature : int = 0.2
    timeout : int = 120
    
    streaming : bool = True