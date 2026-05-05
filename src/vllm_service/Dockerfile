FROM vllm/vllm-openai:latest

ENV HF_HOME=/root/.cache/huggingface
EXPOSE 8000

# Future path to my MlFlow model

CMD ["vllm", "serve", "--model", "/usr/local/model/mylocalmodel"]