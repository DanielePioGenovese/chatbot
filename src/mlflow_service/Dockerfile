FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

COPY src/mlflow_service/main.py src/mlflow_service/settings.py ./
COPY src/mlflow_service/pyproject.toml src/mlflow_service/uv.lock ./

RUN uv sync 

ENV GIT_PYTHON_REFRESH=quiet

CMD ["uv", "run", "-m", "main"]