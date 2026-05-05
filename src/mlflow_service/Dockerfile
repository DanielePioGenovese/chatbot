FROM ghcr.io/mlflow/mlflow:latest

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY src/mlflow_service/main.py src/mlflow_service/settings.py ./
COPY src/mlflow_service/pyproject.toml src/mlflow_service/uv.lock ./

RUN uv sync 

ENV GIT_PYTHON_REFRESH=quiet
