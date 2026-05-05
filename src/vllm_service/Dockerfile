FROM vllm/vllm-openai:latest

ENV HF_HOME=/root/.cache/huggingface
EXPOSE 8000

CMD ["--host", "0.0.0.0", \
     "--port", "8000", \
     "--gpu-memory-utilization", "0.85", \
     "--enforce-eager", \
     "--enable-auto-tool-choice", \
     "--tool-call-parser", "hermes"]