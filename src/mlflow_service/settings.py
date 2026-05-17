from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_id: str = "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4"
    
    mlflow_url: str = "http://mlflow:5000"
    set_experiment: str = "chatbot"
    artifact_path: str = "chatbot_main_model"
    dst_path: str = "/models/main_model"
    log_model_name: str = "main_model"
    main_prompt_name: str = "main_prompt"
    
    prompt_alias: str = "production"
    prompt_main_model: str = """\
        You are a helpful assistant for a small metal parts company.
        Provide the best possible answer based on the context given.
    """
