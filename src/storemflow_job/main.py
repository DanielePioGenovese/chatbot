import mlflow 
from transformers import AutoTokenizer, AutoModelForCausalLM

mlflow.set_experiment('MainModel')
mlflow.set_tracking_uri('http://mflow:5000')

model_id = "Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4"

with mlflow.start_run():

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype="auto"
    )

    mlflow.transformers.log_model(
        transformers_model=model,
        artifact_path="/models",
        input_example="Hi, how can i help you with?",
        metadata={"quantization": "GPTQ-Int4", "base_model": "Qwen2.5-7B"}
    )

    print('Model saved succesfully')

