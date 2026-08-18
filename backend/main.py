from contextlib import asynccontextmanager
from pathlib import Path
from secrets import token_urlsafe

import database
from fastapi import Cookie, Depends, FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

FRONTEND_DIRECTORY = Path(__file__).parent.parent / "frontend" / "out"
active_sessions: set[str] = set()


@asynccontextmanager
async def lifespan(_: FastAPI):
    database.initialize_database()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/api/ping")
def ping():
    return {"status": "ok", "message": "pong"}


class LoginRequest(BaseModel):
    username: str
    password: str


class CardData(BaseModel):
    id: str
    title: str
    details: str


class ColumnData(BaseModel):
    id: str
    title: str
    cardIds: list[str]


class BoardData(BaseModel):
    columns: list[ColumnData]
    cards: dict[str, CardData]


def get_current_username(session_id: str | None = Cookie(default=None)):
    if session_id not in active_sessions:
        raise HTTPException(status_code=401, detail="Authentication required.")
    return "user"


@app.post("/api/login")
def login(credentials: LoginRequest, response: Response):
    if credentials.username != "user" or credentials.password != "password":
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    session_id = token_urlsafe(32)
    active_sessions.add(session_id)
    response.set_cookie("session_id", session_id, httponly=True, samesite="lax")
    return {"username": "user"}


@app.post("/api/logout")
def logout(response: Response, session_id: str | None = Cookie(default=None)):
    if session_id:
        active_sessions.discard(session_id)
    response.delete_cookie("session_id")
    return {"status": "ok"}


@app.get("/api/session")
def session(session_id: str | None = Cookie(default=None)):
    if session_id in active_sessions:
        return {"authenticated": True, "username": "user"}
    return {"authenticated": False}


@app.get("/api/board", response_model=BoardData)
def get_current_board(username: str = Depends(get_current_username)):
    return database.get_board(username)


@app.put("/api/board", response_model=BoardData)
def update_current_board(
    board: BoardData, username: str = Depends(get_current_username)
):
    database.save_board(username, board.model_dump())
    return board


app.mount("/", StaticFiles(directory=FRONTEND_DIRECTORY, html=True), name="frontend")
