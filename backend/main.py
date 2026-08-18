from pathlib import Path
from secrets import token_urlsafe

from fastapi import Cookie, FastAPI, HTTPException, Response
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()
FRONTEND_DIRECTORY = Path(__file__).parent.parent / "frontend" / "out"
active_sessions: set[str] = set()

@app.get("/api/ping")
def ping():
    return {"status": "ok", "message": "pong"}


class LoginRequest(BaseModel):
    username: str
    password: str


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


app.mount("/", StaticFiles(directory=FRONTEND_DIRECTORY, html=True), name="frontend")
