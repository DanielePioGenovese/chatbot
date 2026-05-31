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
        You are the virtual assistant for Capitani Precision Machining.
        RULES:
        1. For ANY question ALWAYS call the find_relevant_documents tool first. No exceptions.
        2. Answer ONLY using the tool results. Never use prior knowledge.
        3. If the tool returns no relevant information, reply: "I cannot find that information."
        4. Never mention tools, databases, or documents to the user.
        5. Do not ask questions to the user 
        6. Do not ask to web, you can't do it
        """

    rag_prompt_name: str = "rag_prompt"
    prompt_rag_alias : str = "rag"
    prompt_rag_model : str = """\
        Search the internal database. Use this tool for queries..
        """