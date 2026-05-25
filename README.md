# Chatbot

Full-stack industrial assistant demo with a React frontend and a Dockerized Python backend for RAG, MCP tools, model serving, and agent inference.

The repository is split into two independent stacks:

- `backend/` contains the Docker Compose setup, Python services, RAG documents, architecture assets, and service-level READMEs.
- `frontend/` contains the Vite React Router app that replaces the previous standalone `website.html` page.

## Contents

- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Backend Services](#backend-services)
- [Frontend App](#frontend-app)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Useful Commands](#useful-commands)
- [Ports](#ports)

## Tech Stack

### Frontend

- React 19
- React Router 7
- Vite 7
- Tailwind CSS 4
- Lucide React icons

### Backend

- Python 3.11+
- FastAPI
- LangChain
- LangChain MCP adapters
- FastMCP
- MLflow
- Qdrant
- FastEmbed
- vLLM OpenAI-compatible server
- Docker Compose
- uv for Python dependency management

## Project Structure

```text
.
├── backend/
│   ├── compose.yaml
│   ├── Makefile
│   ├── docs/
│   ├── architecture/
│   └── src/
│       ├── agent/
│       ├── ingestionrag_service/
│       ├── mcp_server_service/
│       ├── mlflow_service/
│       └── qdrant_service/
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── routes/App.jsx
│       └── styles.css
└── README.md
```

## Backend Services

The backend is orchestrated with Docker Compose from `backend/compose.yaml`.

- `qdrant`: vector database for RAG storage.
- `ingestionrag`: one-shot ingestion job that loads `backend/docs/` into Qdrant.
- `mlflow`: MLflow tracking and artifact server.
- `mlflow-app`: one-shot job that prepares model and prompt artifacts.
- `vllm`: OpenAI-compatible model serving endpoint.
- `mcpserver`: MCP server exposing retrieval and tool capabilities.
- `app`: FastAPI agent service exposed at `http://localhost:9998/agent`.

## Frontend App

The frontend is a React Router single-page app in `frontend/`.

It renders the TechLogic landing page and the floating AI assistant chat widget. The chat widget sends user messages to the backend agent endpoint using this payload:

```json
{
  "prompt": "Your question here"
}
```

By default, the frontend calls:

```text
http://localhost:9998/agent
```

## Quick Start

### 1. Start the backend

```bash
cd backend
make up
```

This starts the infrastructure, ingestion jobs, MCP server, model server, and FastAPI agent service.

### 2. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the terminal, usually:

```text
http://localhost:5173/
```

## Configuration

### Frontend

Set `VITE_BACKEND_URL` if the agent API is not running on the default local URL.

Example:

```bash
VITE_BACKEND_URL=http://localhost:9998/agent npm run dev
```

### Backend

The Compose stack reads `HF_TOKEN` for Hugging Face access when needed:

```bash
HF_TOKEN=your_token_here make up
```

Model files and generated runtime data are expected under backend-local folders such as:

- `backend/models/`
- `backend/model_weights/`
- `backend/mlruns/`
- `backend/qdrant_data/`

These paths are intentionally ignored by Git.

## Useful Commands

### Backend

Run from `backend/`.

```bash
make up          # Start the full backend stack
make down        # Stop containers
make build       # Build Docker images
make rebuild     # Rebuild and restart only the app service
make ingest      # Re-run document ingestion
make populate    # Re-run MLflow artifact population
make logs        # Follow app and MCP server logs
make logs-all    # Follow all service logs
make ps          # Show Compose service status
make clean       # Stop containers and remove Compose volumes
```

### Frontend

Run from `frontend/`.

```bash
npm install      # Install dependencies
npm run dev      # Start Vite dev server
npm run build    # Build production assets
npm run preview  # Preview the production build
```

## Ports

| Service | URL | Purpose |
| --- | --- | --- |
| Frontend | `http://localhost:5173/` | Vite React app |
| Agent API | `http://localhost:9998/agent` | FastAPI chat endpoint |
| MCP server | `http://localhost:8021/mcp` | MCP tool server |
| MLflow | `http://localhost:5001/` | Tracking and artifact UI |
| Qdrant HTTP | `http://localhost:6333/` | Vector database API |
| Qdrant gRPC | `localhost:6334` | Vector database gRPC |
| vLLM | `http://localhost:8222/` | OpenAI-compatible model server |

## Notes

- Start the backend before using the chat widget, otherwise the frontend will show `Connection error`.
- The backend stack is GPU-oriented for `vllm` and `ingestionrag`, so Docker with NVIDIA runtime support is expected for the full stack.
- Service-specific implementation notes live in each backend service folder under `backend/src/`.
