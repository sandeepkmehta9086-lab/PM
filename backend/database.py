import json
import os
import sqlite3
from contextlib import closing
from pathlib import Path

DATABASE_PATH = Path(
    os.environ.get("DATABASE_PATH", Path(__file__).parent.parent / "data" / "pm.db")
)
DEFAULT_BOARD_PATH = Path(__file__).with_name("default_board.json")

SCHEMA = """
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
"""


def connect():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with closing(connect()) as connection, connection:
        connection.executescript(SCHEMA)
        connection.execute("INSERT OR IGNORE INTO users (username) VALUES ('user')")


def get_board(username: str):
    with closing(connect()) as connection, connection:
        row = connection.execute(
            """
            SELECT boards.data_json
            FROM boards
            JOIN users ON users.id = boards.user_id
            WHERE users.username = ?
            """,
            (username,),
        ).fetchone()

        if row:
            return json.loads(row["data_json"])

        board = json.loads(DEFAULT_BOARD_PATH.read_text())
        connection.execute(
            """
            INSERT INTO boards (user_id, data_json)
            SELECT id, ? FROM users WHERE username = ?
            """,
            (json.dumps(board), username),
        )
        return board


def save_board(username: str, board: dict):
    with closing(connect()) as connection, connection:
        connection.execute(
            """
            INSERT INTO boards (user_id, data_json)
            SELECT id, ? FROM users WHERE username = ?
            ON CONFLICT(user_id) DO UPDATE SET
                data_json = excluded.data_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (json.dumps(board), username),
        )
