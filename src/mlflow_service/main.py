import mlflow 
from settings import Settings
from huggingface_hub import snapshot_download
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

s = Settings()

mlflow.set_tracking_uri(s.mlflow_url)
mlflow.set_experiment(s.set_experiment)

logger.info(f"Downloading model {s.model_id} to {s.dst_path}...")
snapshot_download(repo_id=s.model_id, local_dir=s.dst_path)
logger.info("Model downloaded correctly!")

with mlflow.start_run():

    mlflow.log_params({
        "model_id": s.model_id,
        "model_path": s.dst_path,
    })
    
    logger.info("Model reference logged to MLflow")
    
    prompt = mlflow.genai.register_prompt(
        name=s.main_prompt_name,
        template=s.prompt_main_model,
        commit_message="Init main prompt",
    )
    logger.info("Prompt created successfully!")

    client = mlflow.MlflowClient()
    client.set_prompt_alias(                  
        name=s.main_prompt_name,
        alias=s.prompt_alias,
        version=prompt.version             
        )