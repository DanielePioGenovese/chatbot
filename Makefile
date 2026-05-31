.PHONY: up down build rebuild logs ps clean ingest populate app

# ── Default ────────────────────────────────────────────────────────────────

up:                             ## Start the full stack (infra → jobs → app)
	docker compose up -d

down:                           ## Stop and remove all containers
	docker compose down

build_up:
	docker compose up --build

restart_app:
	docker compose restart app

# ── Build ──────────────────────────────────────────────────────────────────

build:                          ## Build all images without starting
	docker compose build

rebuild:                        ## Rebuild and restart only the app (no deps recreated)
	docker compose up -d --build --no-deps app

# ── One-shot jobs (run manually if needed) ─────────────────────────────────

ingest:                         ## Re-run ingestion into Qdrant
	docker compose run --rm ingestionrag

populate:                       ## Re-run MLflow model/prompt upload
	docker compose run --rm mlflow-app

# ── Observability ──────────────────────────────────────────────────────────

logs:                           ## Tail logs for app + mcpserver
	docker compose logs -f app mcpserver

logs-all:                       ## Tail all service logs
	docker compose logs -f

ps:                             ## Show container status
	docker compose ps

# ── Cleanup ────────────────────────────────────────────────────────────────

clean:                          ## Stop containers and wipe volumes
	docker compose down -v
	docker system prune -f