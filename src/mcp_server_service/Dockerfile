FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app


=COPY src/mcp_server_service/pyproject.toml src/mcp_server_service/uv.lock ./

RUN uv sync --frozen --no-dev

COPY src/mcp_server_service/ .

EXPOSE 6000

CMD ["uv", "run", "python", "main.py"]