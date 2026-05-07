import mlflow 
from transformers import AutoTokenizer
from settings import Settings
import logging

logger = logging.getLogger(__name__)

s = Settings()

mlflow.set_tracking_uri('http://localhost:5000')
mlflow.set_experiment('chatbot')

with mlflow.start_run():

    tokenizer = AutoTokenizer.from_pretrained(s.model_id)

    components = {
        "model": s.model_id,
        "tokenizer": tokenizer,
    }

    mlflow.transformers.log_model(
        transformers_model=components,
        artifact_path="model_artifacts",
        task="text-generation",
        input_example="Hi, how can i help you with?",
        metadata={"quantization": "GPTQ-Int4", "base_model": "Qwen2.5-7B"}
    )

    prompt = mlflow.genai.register_prompt(
        name=s.prompt_name,
        template=s.initial_template,
    )

    logger.info(f'Model: and Prompt: {prompt.name} saved succesfully!')
