FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

COPY src/storemlflow_job/main.py src/storemlflow_job/settings.py ./
COPY src/storemlflow_job/pyproject.toml src/storemlflow_job/uv.lock ./

RUN uv sync 

ENV GIT_PYTHON_REFRESH=quiet

CMD ["uv", "run", "-m", "main"]