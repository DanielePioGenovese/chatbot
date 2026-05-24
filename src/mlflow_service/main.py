import mlflow 
from settings import Settings
from huggingface_hub import snapshot_download
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

# Initialize the application configuration object
s = Settings()

mlflow.set_tracking_uri(s.mlflow_url)
mlflow.set_experiment(s.set_experiment)

logger.info(f"Downloading model {s.model_id} to {s.dst_path}...")
# Download the complete repository snapshot (weights, tokenizer, configs) from Hugging Face Hub
snapshot_download(repo_id=s.model_id, local_dir=s.dst_path)
logger.info("Model downloaded correctly!")

# Begin an MLflow tracking run to record parameters, artifacts, and prompts metadata
with mlflow.start_run():

    # Log the foundational metadata regarding the downloaded model's identity and storage location
    mlflow.log_params({
        "model_id": s.model_id,
        "model_path": s.dst_path,
    })
    
    logger.info("Model reference logged to MLflow")
    
    # Register the system prompt template for the main model inside the MLflow GenAI Prompt Registry
    prompt = mlflow.genai.register_prompt(
        name=s.main_prompt_name,
        template=s.prompt_main_model,
        commit_message="Init main prompt",
    )
    logger.info("Main prompt created successfully!")

    # Register the baseline system prompt template specifically configured for the RAG architecture
    prompt_rag = mlflow.genai.register_prompt(
        name=s.rag_prompt_name,
        template=s.prompt_rag_model,
        commit_message="Init main rag prompt",
    )
    logger.info("RAG prompt created successfully!")
    logger.info(print(prompt_rag))
    
    # Initialize the low-level MLflow Client API to interact directly with backend tracking metadata
    client = mlflow.MlflowClient()
    
    # Assign a deployment/production alias to the specific version of the registered main prompt
    client.set_prompt_alias(                  
        name=s.main_prompt_name,
        alias=s.prompt_alias,
        version=prompt.version             
    )

    # Assign a deployment/production alias to the specific version of the registered RAG prompt
    client.set_prompt_alias(                  
        name=s.rag_prompt_name,
        alias=s.prompt_rag_alias,
        version=prompt_rag.version             
    )