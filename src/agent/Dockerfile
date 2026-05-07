FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY src/agent/pyproject.toml src/agent/uv.lock ./

RUN uv sync

CMD ["uv", "run", "fastapi", "run", "main.py"]