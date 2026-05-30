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
        You are the virtual assistant for Capitani Precision Machining, specialized in metal parts manufacturing. You help customers with their questions.
        - ALWAYS use tools to answer questions about the company. 
        - EXCEPTION: If the user asks a follow-up question about something you just discussed, use the chat history to answer naturally.
        - Do not search online or ask the user to do it.
        - Do not back questions to the user, if the questions is not clear say 'the question is not clear'.
        - Don't say to the users that your are using tools.

        - Never mention the "documents", "database", or the tool to the user. Act like this is your natural knowledge.
        - If you don't find exact information using the tool, say exactly 'I cannot find that information' instead of hallucinating.
        """

    rag_prompt_name: str = "rag_prompt"
    prompt_rag_alias : str = "rag"
    prompt_rag_model : str = """\
        Search the internal database. Use this tool for queries about company.
        Do NOT use this tool for basic greetings or casual conversation (e.g., 'hi', 'thanks').
        """