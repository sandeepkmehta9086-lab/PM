# Project Management MVP

A local project management app built around a Kanban board and AI-assisted card management.

## Status

The frontend is statically built and served by the FastAPI backend in Docker. It supports sign in, local Kanban interactions, including drag and drop, column renaming, card management, and logout.

The backend persists one board per user in SQLite, and the frontend synchronizes board changes through the API. The AI chat sidebar displays OpenRouter responses and applies validated board updates.

Set `OPENROUTER_API_KEY` in a root `.env` file to enable the backend AI connectivity endpoint.

## Planned stack

- Next.js frontend
- FastAPI backend
- SQLite database
- Docker for local execution
- OpenRouter using `openai/gpt-oss-120b`

## MVP credentials

Use:

- Username: `user`
- Password: `password`

See `docs/PLAN.md` for the implementation plan.
