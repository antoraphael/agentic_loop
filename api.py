"""FastAPI bridge between the React UI and the local Ollama agent."""

import logging
import uuid
from threading import Lock

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from main import run_agent
from messages import create_messages

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Local Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Demo-only session storage. This is cleared when the backend restarts.
# For production, use a database or persistent LangGraph checkpointer.
_sessions: dict[str, list[dict]] = {}
_sessions_lock = Lock()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    session_id: str


@app.get("/health")
def health():
    return {"status": "ok", "service": "local-agent-api"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    session_id = request.session_id or str(uuid.uuid4())

    with _sessions_lock:
        if session_id not in _sessions:
            # create_messages starts with system + user. Remove the empty user
            # message so run_agent can append the actual request.
            history = create_messages("")
            history.pop()
            _sessions[session_id] = history
        history = _sessions[session_id]

    try:
        answer = run_agent(user_message, messages=history)
        return ChatResponse(answer=answer, session_id=session_id)
    except Exception as error:
        logger.exception("Agent request failed")
        raise HTTPException(
            status_code=500,
            detail=f"Agent failed: {error}",
        ) from error


@app.delete("/sessions/{session_id}")
def clear_session(session_id: str):
    with _sessions_lock:
        _sessions.pop(session_id, None)
    return {"status": "cleared", "session_id": session_id}
