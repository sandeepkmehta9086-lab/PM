# Backend Agent Notes

## Purpose
This backend serves the Project Management MVP with FastAPI, static frontend hosting, basic API routes, and Docker support.

## Current implementation
- `backend/main.py` provides a FastAPI app.
- `GET /api/ping` returns `{ "status": "ok", "message": "pong" }`.
- `POST /api/login` authenticates `user` / `password` and sets an HTTP-only session cookie.
- `GET /api/session` reports whether the current session is authenticated.
- `POST /api/logout` clears the current session.
- `GET /` serves the statically exported Next.js app from `frontend/out`.

## Backend packaging
- `pyproject.toml` declares `fastapi` and `uvicorn[standard]` dependencies.
- `backend/Dockerfile` builds the frontend, installs backend dependencies with `uv`, and runs Uvicorn on port 8000.
- `docker-compose.yml` builds the combined app image and forwards port `8000:8000`.

## Scripts
- `scripts/start.ps1` and `scripts/start.sh` launch Docker Compose.
- `scripts/stop.ps1` and `scripts/stop.sh` stop Docker Compose.

## Notes
- Authentication sessions are in memory and are intentionally temporary until the database is added.
- The current board is still client-only and has no persistence API.
