# Chatbot

This project is now split into two independent stacks:

- `backend/` contains the Docker Compose setup, Python services, documentation, and architecture assets.
- `frontend/` contains the React Router app that replaces the previous `website.html` page.

## Backend

```bash
cd backend
make up
```

The agent API is exposed at `http://localhost:9998/agent`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend reads `VITE_BACKEND_URL` when set, otherwise it uses `http://localhost:9998/agent`.
