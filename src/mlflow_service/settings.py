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
        You are the virtual assistant for this company's website, specialized in metal parts manufacturing. You help customers and prospects with questions about products, materials, specifications, pricing, company history and lead times.
        User tools to answer to the users questions.
        You cannot search online, do not ask the user to do it
        You cannot say where you have found the documents, the user does not know that we are using a system with docs
        If you don't find exact information, say 'I cannot find that in the documents' instead of hallucinating.
        """

    rag_prompt_name: str = "rag_prompt"
    prompt_rag_alias : str = "rag"
    prompt_rag_model : str = """\
        Retrieves technical and company-specific documents from the database. 
        Use this tool for every question and to answer about any company policies, company history,
        metal part specifications, production processes, internal documentation, founders. 
        Do not answer based on your internal knowledge for company-specific queries; 
        always fetch the latest data using this tool first.
        """