# Database schema

The application will use a local SQLite database. It supports multiple users,
while the MVP permits one board per user.

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS boards (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL UNIQUE,
  data_json TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

`boards.user_id` is unique, enforcing the MVP rule that each user owns one
board. `data_json` stores the entire board payload rather than splitting board
state across tables. This retains the existing column order, each column's card
order, renamed column titles, and card details.

## Board JSON format

`data_json` contains the frontend `BoardData` object without transformation:

```json
{
  "columns": [
    {
      "id": "col-backlog",
      "title": "Backlog",
      "cardIds": ["card-1"]
    }
  ],
  "cards": {
    "card-1": {
      "id": "card-1",
      "title": "Align roadmap themes",
      "details": "Draft quarterly themes with impact statements and metrics."
    }
  }
}
```

- `columns` is an ordered array of `{ id, title, cardIds }` objects.
- `cards` is an object keyed by card ID. Each card has `id`, `title`, and
  `details`.
- The backend will validate and serialize this shape when board APIs are added.

## Initialization and lifecycle

FastAPI initializes `data/pm.db` on startup, creating tables and the hardcoded
MVP `user` when missing. Docker persists that directory in its `app-data`
volume.

`GET /api/board` lazily seeds the user's first board from
`backend/default_board.json`, which matches the frontend `initialData`.
`PUT /api/board` replaces `data_json` and updates `updated_at`.
