FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

COPY src/agent/pyproject.toml src/agent/uv.lock ./
COPY src/agent/main.py src/agent/settings.py src/agent/agent.py src/agent/validator.py ./

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "9998"]

