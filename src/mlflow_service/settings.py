from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_id : str = "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4"

    initial_template : str = "You are an helpful assitant for a small metal parts industry"
    prompt_name : str = "rag-assistant"

    mlflow_url : str = 'http://mlflow-server:5000'
    set_experiment : str = "chatbot"

    artifact_path : str = "chatbot_main_model"
    dst_path : str = "/models/main_model" 

    log_model_name : str = "main_model"

    main_prompt_name : str = 'main_prompt'
    prompt_main_model : str = """\
        You are an helpful asssistant for a small metal parts company, you have to give back
        the best possible answer.
    """
