# Backend Agent Notes

## Purpose
This backend serves the Project Management MVP with FastAPI, static frontend hosting, basic API routes, and Docker support.

## Current implementation
- `backend/main.py` provides a FastAPI app.
- `GET /api/ping` returns `{ "status": "ok", "message": "pong" }`.
- `POST /api/login` authenticates `user` / `password` and sets an HTTP-only session cookie.
- `GET /api/session` reports whether the current session is authenticated.
- `POST /api/logout` clears the current session.
- `GET /api/board` returns the authenticated user's JSON-backed board.
- `PUT /api/board` validates and persists the authenticated user's board.
- `POST /api/ai/test` requires authentication and asks OpenRouter `2+2`.
- `POST /api/ai/chat` sends the saved board and conversation history to OpenRouter, then optionally persists a validated board replacement.
- `GET /` serves the statically exported Next.js app from `frontend/out`.

## Backend packaging
- `pyproject.toml` declares `fastapi` and `uvicorn[standard]` dependencies.
- `backend/Dockerfile` builds the frontend, installs backend dependencies with `uv`, and runs Uvicorn on port 8000.
- `docker-compose.yml` builds the combined app image, forwards port `8000:8000`, and stores SQLite data in a named volume.

## Scripts
- `scripts/start.ps1` and `scripts/start.sh` launch Docker Compose.
- `scripts/stop.ps1` and `scripts/stop.sh` stop Docker Compose.

## Notes
- SQLite data is initialized at `data/pm.db`; users own one JSON-backed board.
- Authentication sessions remain in memory; the frontend uses the board APIs for persistence.
- OpenRouter uses `openai/gpt-oss-120b` and requires `OPENROUTER_API_KEY`.
- AI responses use a strict `{ response, boardUpdate }` schema; `boardUpdate` is either null or a complete validated board.
