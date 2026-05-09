import mlflow 
from settings import Settings
from transformers import AutoModelForMaskedLM, AutoTokenizer
import logging

logger = logging.getLogger(__name__)

s = Settings()

mlflow.set_tracking_uri(s.mlflow_url)
mlflow.set_experiment(s.set_experiment)

tokenizer = AutoTokenizer.from_pretrained(s.model_id)
model = AutoModelForMaskedLM.from_pretrained(s.model_id)

with mlflow.start_run():

    components = {
        'model' : model,
        'tokenizer' : tokenizer,
    }

    mlflow.transformers.log_model(
        transformers_model=components, 
        name=s.log_model_name
    )
    
    logger.info('Model saved succesfully')

    run_id = mlflow.active_run().info.run_id
    logger.info(f"Moving the model for the id {run_id}")

    mlflow.artifacts.download_artifacts(
        run_id=run_id,
        artifac_path=s.artifact_path,
        dst_path=s.dst_path
    )

    logger.info("Model downloaded correctly")

    # Prompt

    prompt = mlflow.genai.register_prompt(
        name=s.main_prompt_name,
        tempalte=s.prompt_main_model,
        commit_message='Init main prompt',
    )

    logger.info(f"Created the correctly the prompt")