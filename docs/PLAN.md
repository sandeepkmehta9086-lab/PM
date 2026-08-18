# High level steps for project

## Testing approach

Add tests for valuable behavior, regressions, and integration risks. Aim for roughly 80% coverage when practical, but do not add low-value tests solely to meet a coverage target.

Part 1: Plan

- Review the repository structure and current frontend implementation.
- Confirm the MVP scope, stack decisions, and overall deliverables against `AGENTS.md`.
- Create `frontend/AGENTS.md` documenting the existing frontend code, architecture, and tests.
- Consolidate implementation notes in the root `AGENTS.md` so the plan reflects the current state.
- Define the work breakdown for Parts 2 through 10 with explicit substeps, checkpoints, and required tests.
- Present the plan for user review and approval before any code changes beyond planning.

Checklist:
- [x] Review current repo and frontend state
- [x] Create `frontend/AGENTS.md`
- [x] Update root `AGENTS.md` with implementation notes and next steps
- [x] Confirm the plan with the user
- [x] Finalize the plan and begin Part 2 after approval

Success criteria:
- The plan clearly describes what will be built in each part and how it will be tested.
- The project scope is aligned with the root `AGENTS.md` and the existing frontend demo.
- The user has reviewed and approved the plan explicitly.
- There is a concrete handoff point from planning to implementation.

Part 2: Scaffolding

- Scaffold the backend in `backend/` using FastAPI.
- Add a simple `main.py` or `app.py` that starts a FastAPI app and exposes HTTP endpoints.
- Add a Dockerfile for the Python backend and a root-level `docker-compose.yml` or equivalent container launch configuration.
- Add cross-platform start/stop scripts in `scripts/` for Windows, Mac, and Linux.
- Implement a placeholder route such as `/api/ping` that returns JSON and a static route that serves example HTML.
- Verify the backend can start locally and responds correctly.

Checklist:
- [x] Create backend scaffold in `backend/`
- [x] Add Dockerfile and/or compose configuration
- [x] Add start/stop scripts in `scripts/`
- [x] Implement `/api/ping` and static HTML serving
- [x] Verify the app runs locally and responds to HTTP requests

Tests:
- Run backend startup locally and confirm no immediate errors.
- Request `/api/ping` and verify JSON response.
- Request `/` and verify the placeholder HTML content.

Success criteria:
- The backend starts under Docker and/or locally.
- `GET /api/ping` returns a 200 JSON payload.
- `GET /` returns static HTML content.
- The start/stop scripts work for the target OSes.

Part 3: Add in Frontend

- Build the existing Next.js frontend with `npm run build`.
- Integrate the built frontend into the backend static serving path.
- Update the backend so `GET /` serves the Next.js app from the build output.
- Confirm the Kanban demo loads from the backend at `/`.
- Preserve the existing frontend behavior while enabling static hosting.

Checklist:
- [x] Build the frontend successfully
- [x] Configure the backend to serve the frontend output
- [x] Confirm `/` displays the Kanban board
- [x] Keep existing demo UI and interactions unchanged

Tests:
- Build the frontend with `npm run build`.
- Start the backend and access `/`.
- Verify the page renders with `Kanban Studio` and five columns.

Success criteria:
- Frontend build passes.
- Backend serves the static frontend at `/`.
- The Kanban board renders correctly from the integrated backend.

Part 4: Add in a fake user sign in experience

- Add a login page or modal to the frontend.
- Add backend login and logout endpoints.
- Use a simple fake auth flow for credentials `user` / `password`.
- Allow a logged-in user to view the Kanban and log out.
- Prevent unauthenticated access to the board.

Checklist:
- [x] Add login UI and auth state handling in frontend
- [x] Add `/api/login` and `/api/logout` endpoints in backend
- [x] Protect board access for unauthenticated users
- [x] Add logout support

Tests:
- Unit test login page behavior.
- E2E test login with valid credentials and verify board access.
- E2E test invalid credentials are rejected.
- E2E test logout returns user to login.

Success criteria:
- Unauthenticated users cannot see the board.
- Valid dummy credentials authenticate successfully.
- Logout clears auth and returns to login.

Part 5: Database modeling

- Design a SQLite schema for users and Kanban boards.
- Store the board as JSON to preserve columns, cards, and metadata.
- Document the schema and persistence approach in `docs/`.
- Ensure the database is created automatically if missing.

Checklist:
- [ ] Define SQL schema for users and board state
- [ ] Document the schema in `docs/`
- [ ] Implement automatic DB creation on startup
- [ ] Use JSON storage for board payloads

Tests:
- Validate the schema document and the DB schema match.
- Start the backend and confirm the SQLite file is created.
- Confirm the DB contains the expected tables.

Success criteria:
- There is a documented SQLite schema in `docs/`.
- The app creates the SQLite database automatically.
- Board data is stored as JSON in the DB.

Part 6: Backend

- Add backend API routes to read and update the Kanban board for the authenticated user.
- Implement persistence using SQLite and the schema from Part 5.
- Ensure board updates are saved and can be reloaded.

Checklist:
- [ ] Add `GET /api/board` for the current user
- [ ] Add `PUT /api/board` or `PATCH /api/board` to save board state
- [ ] Implement DB persistence and user lookup
- [ ] Add backend unit tests for API routes

Tests:
- Backend tests for `GET /api/board` returning the current board.
- Backend tests for saving board state and retrieving the saved value.
- Tests ensure the DB is created if it does not exist.

Success criteria:
- The backend can read and write the user’s board.
- Persistence works across backend restarts.
- Unit tests cover the API routes and persistence behavior.

Part 7: Frontend + Backend

- Update the frontend to use backend APIs for auth and board state.
- Load the board from `GET /api/board` on authenticated startup.
- Save board changes through the backend API.
- Keep the existing UX and board interactions intact.

Checklist:
- [ ] Load board state from backend on app startup
- [ ] Save board state to backend on relevant changes
- [ ] Keep local drag/drop, rename, add, delete UX
- [ ] Add paired frontend/backend integration tests

Tests:
- Unit tests for API integration and board state flow.
- E2E tests validating board data persists across refreshes.
- E2E test that changes made in the UI are stored in backend state.

Success criteria:
- The app loads board data from the backend.
- Board edits persist through backend API calls.
- The UI remains consistent with the existing demo.

Part 8: AI connectivity

- Add OpenRouter integration to the backend.
- Add `OPENROUTER_API_KEY` support from environment.
- Build a simple backend AI test endpoint that sends a `2+2` prompt and returns the result.

Checklist:
- [ ] Add OpenRouter client support in backend
- [ ] Read `OPENROUTER_API_KEY` from environment
- [ ] Add a simple AI test endpoint
- [ ] Verify the backend can call the AI service

Tests:
- Backend unit test for the AI request/response logic, using a mock OpenRouter call.
- Manual or integration test for real API connectivity if the key is available.

Success criteria:
- The backend can call OpenRouter and receive a valid response.
- A `2+2` endpoint returns the expected answer.
- The AI integration is isolated and testable.

Part 9: Structured AI board updates

- Extend the backend AI call to include the current board JSON, the user question, and conversation history.
- Define a structured output format with `response` and optional `boardUpdate` payload.
- Parse the AI response safely and apply board updates when provided.

Checklist:
- [ ] Define the structured AI response contract
- [ ] Send board JSON and history with each AI request
- [ ] Parse and validate the AI response
- [ ] Update the board when the AI returns changes
- [ ] Add backend tests for parsing and update behavior

Tests:
- Unit tests for structured response parsing.
- Unit tests for board update application based on AI payloads.
- Fallback tests for invalid or missing update fields.

Success criteria:
- AI responses are returned in a predictable structured format.
- The backend can apply optional board updates from the AI.
- Invalid AI output is handled safely.

Part 10: AI chat sidebar

- Add a UI sidebar for chat messages and user prompts.
- Display the AI response text and any board update confirmations.
- Allow the AI to update the board and refresh the UI automatically.
- Keep the chat visually integrated with the existing Kanban experience.

Checklist:
- [ ] Add chat sidebar UI and input controls
- [ ] Connect the chat UI to the backend AI endpoint
- [ ] Display conversation history
- [ ] Apply board updates and refresh the board state
- [ ] Add UI and E2E tests for the chat feature

Tests:
- Component tests for chat input and message rendering.
- E2E tests covering a chat request, AI response, and board update.
- Verify board refreshes automatically after AI-triggered changes.

Success criteria:
- The app includes an AI chat sidebar.
- Users can ask questions and receive AI responses.
- AI-suggested board updates are reflected immediately in the UI.