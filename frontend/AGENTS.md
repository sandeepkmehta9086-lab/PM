# Frontend Agent Notes

## Purpose
This document describes the current frontend implementation for the Project Management MVP app and summarizes the key files, features, and test coverage.

## Current Implementation
- Framework: Next.js 16.1.6
- UI: React 19 with Tailwind CSS v4
- Drag and drop: @dnd-kit core + sortable
- State: authenticated board data is loaded and saved through the backend API.
- Data model: `BoardData` with columns and cards defined in `src/lib/kanban.ts`

## Core UI
- `src/app/page.tsx`
  - Renders `App`, which gates the board on the current session.

- `src/components/App.tsx`
  - Checks the backend session, loads the board, saves board changes, and handles logout.

- `src/components/LoginForm.tsx`
  - Submits the hardcoded MVP credentials to the backend and displays rejected-login feedback.

- `src/components/ChatSidebar.tsx`
  - Displays conversation history and sends prompts to the structured AI chat endpoint.

- `src/components/KanbanBoard.tsx`
  - Renders the API-backed board, chat sidebar, and emits drag-and-drop, rename, add, and delete changes.
  - Uses `DndContext` and `DragOverlay`.
  - Builds UI with a single board, five columns, and an app shell.

- `src/components/KanbanColumn.tsx`
  - Renders a droppable column.
  - Supports inline title editing, card listing, and new card creation.

- `src/components/KanbanCard.tsx`
  - Renders a sortable card with drag handles and delete action.

- `src/components/NewCardForm.tsx`
  - Manages open/close form state for creating new cards.
  - Validates title and resets after submission.

## Data and utilities
- `src/lib/kanban.ts`
  - Defines types: `Card`, `Column`, `BoardData`.
  - Provides `initialData` for demo board state.
  - Implements `moveCard` for same-column reorder and column moves.
  - Includes `createId` helper for new cards.

## Tests
- Unit / component tests
  - `src/components/KanbanBoard.test.tsx`
    - Verifies render of columns, rename behavior, add/remove card workflow.
  - `src/lib/kanban.test.ts`
    - Verifies `moveCard` logic for reorder, moving between columns, and end-of-column drops.
  - `src/components/LoginForm.test.tsx`
    - Verifies successful and rejected login submissions.
  - `src/components/App.test.tsx`
    - Verifies that an authenticated session loads its saved board.
  - `src/components/ChatSidebar.test.tsx`
    - Verifies prompt submission and AI message rendering.

- E2E tests
  - `frontend/tests/kanban.spec.ts`
    - Verifies authentication, chat-driven board refresh, logout, card creation persistence, and drag-and-drop between columns.

## Scripts
- `package.json`
  - `dev`: `next dev`
  - `build`: `next build`, generating a static export in `out/`
  - `start`: `next start`
  - `test`: `vitest run`
  - `test:e2e`: builds the static export and runs Playwright against FastAPI

## Notes for next work
- `next.config.ts` configures a static export, which FastAPI serves from `frontend/out`.
- The frontend uses authenticated board APIs to load and save the board.
- AI replies and board updates are applied immediately through the chat sidebar.
