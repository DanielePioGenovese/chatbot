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
        name="Main_model"
    )
    
    logger.info('Model saved succesfully')