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

    rag_prompt_name: str = "rag_prompt"
    prompt_rag_alias : str = "rag"
    prompt_rag_model : str = """\
        Retrieves technical and company-specific documents from the Qdrant database. 
        YOU MUST USE THIS TOOL to answer any questions about company policies, 
        metal part specifications, production processes, or internal documentation. 
        Do not answer based on your internal knowledge for company-specific queries; 
        always fetch the latest data using this tool first.
        When using the 'find_relevant_documents' tool, summarize the findings in 1-2 sentences. 
        Do not list every detail unless specifically asked. 
        If you don't find exact information, say 'I cannot find that in the documents' instead of hallucinating.
        You cannot search online, do not ask the user to do it
        You cannot say where you have found the documents, the user does not know that we are using a system with docs
        """