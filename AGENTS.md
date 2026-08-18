# The Project Management MVP web app

## Business Requirements

This project is building a Project Management App. Key features:
- A user can sign in
- When signed in, the user sees a Kanban board representing their project
- The Kanban board has fixed columns that can be renamed
- The cards on the Kanban board can be moved with drag and drop, and edited
- There is an AI chat feature in a sidebar; the AI is able to create / edit / move one or more cards

## Limitations

For the MVP, there will only be a user sign in (hardcoded to 'user' and 'password') but the database will support multiple users for future.

For the MVP, there will only be 1 Kanban board per signed in user.

For the MVP, this will run locally (in a docker container)

## Technical Decisions

- NextJS frontend
- Python FastAPI backend, including serving the static NextJS site at /
- Everything packaged into a Docker container
- Use "uv" as the package manager for python in the Docker container
- Use OpenRouter for the AI calls. An OPENROUTER_API_KEY is in .env in the project root
- Use `openai/gpt-oss-120b` as the model
- Use SQLLite local database for the database, creating a new db if it doesn't exist
- Start and Stop server scripts for Mac, PC, Linux in scripts/

## Starting Point

A working MVP of the frontend has been built and is already in frontend. This is not yet designed for the Docker setup. It's a pure frontend-only demo.

## Current implementation notes

- The frontend is a standalone Next.js app under `frontend/`.
- The homepage currently renders a client-only `KanbanBoard` component with local state, drag-and-drop, column rename, add card, and delete card behavior.
- The board data model is defined in `frontend/src/lib/kanban.ts` and includes `columns`, `cards`, `moveCard`, and `createId` utilities.
- Tests are already present for component behavior and drag-and-drop logic (`frontend/src/components/KanbanBoard.test.tsx`, `frontend/src/lib/kanban.test.ts`) plus Playwright e2e coverage (`frontend/tests/kanban.spec.ts`).
- The Next.js app is statically exported and served by FastAPI at `/` in the Docker container.
- Fake authentication uses `user` / `password`, HTTP-only in-memory session cookies, and a frontend login gate.
- SQLite stores one JSON-backed board for each user, and the backend exposes authenticated board read/write APIs.
- The frontend loads and saves board changes through the authenticated board APIs.
- The backend includes a verified authenticated OpenRouter connectivity endpoint using `openai/gpt-oss-120b`.
- The backend accepts structured AI chat responses and persists an optional full-board update.
- The frontend includes a chat sidebar that displays AI replies and applies returned board updates immediately.

## Next work

- The MVP implementation is complete.

## Color Scheme

- Accent Yellow: `#ecad0a` - accent lines, highlights
- Blue Primary: `#209dd7` - links, key sections
- Purple Secondary: `#753991` - submit buttons, important actions
- Dark Navy: `#032147` - main headings
- Gray Text: `#888888` - supporting text, labels

## Coding standards

1. Use latest versions of libraries and idiomatic approaches as of today
2. Keep it simple - NEVER over-engineer, ALWAYS simplify, NO unnecessary defensive programming. No extra features - focus on simplicity.
3. Be concise. Keep README minimal. IMPORTANT: no emojis ever
4. When hitting issues, always identify root cause before trying a fix. Do not guess. Prove with evidence, then fix the root cause.

## Working documentation

All documents for planning and executing this project will be in the docs/ directory.
Please review the docs/PLAN.md document before proceeding.