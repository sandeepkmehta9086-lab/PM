# Frontend Agent Notes

## Purpose
This document describes the current frontend implementation for the Project Management MVP app and summarizes the key files, features, and test coverage.

## Current Implementation
- Framework: Next.js 16.1.6
- UI: React 19 with Tailwind CSS v4
- Drag and drop: @dnd-kit core + sortable
- State: client-only state in `KanbanBoard` using React `useState`
- Data model: `BoardData` with columns and cards defined in `src/lib/kanban.ts`

## Core UI
- `src/app/page.tsx`
  - Renders `App`, which gates the board on the current session.

- `src/components/App.tsx`
  - Checks the backend session, renders the login form for unauthenticated users, and handles logout.

- `src/components/LoginForm.tsx`
  - Submits the hardcoded MVP credentials to the backend and displays rejected-login feedback.

- `src/components/KanbanBoard.tsx`
  - Manages board state, drag-and-drop, column rename, add card, delete card, and logout control.
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

- E2E tests
  - `frontend/tests/kanban.spec.ts`
    - Verifies authentication, logout, card creation, and drag-and-drop between columns.

## Scripts
- `package.json`
  - `dev`: `next dev`
  - `build`: `next build`, generating a static export in `out/`
  - `start`: `next start`
  - `test`: `vitest run`
  - `test:e2e`: builds the static export and runs Playwright against FastAPI

## Notes for next work
- `next.config.ts` configures a static export, which FastAPI serves from `frontend/out`.
- The frontend uses authentication APIs but does not yet load or save board data through an API.
- It uses local client state only, so persistence and backend integration are not implemented.
- Future work should preserve the current UI patterns while adding API calls, auth, and server-backed board state.
