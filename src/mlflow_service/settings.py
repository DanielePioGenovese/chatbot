from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_id : str = "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4"

    initial_template : str = "You are an helpful assitant for a small metal parts industry"
    prompt_name : str = "rag-assistant"

    mlflow_url : str = 'http://mlflow-server:5000'
    set_experiment : str = "chatbot"