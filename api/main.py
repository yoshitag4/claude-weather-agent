import uuid
from threading import Lock

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agent.claude_agent import ClaudeAgent
from schemas import ALL_TOOLS
from models.message_models import ChatRequest, ChatResponse, HealthResponse

app = FastAPI(
    title="Claude Weather Agent API",
    version="1.0.0",
)

# Allow the local Vite dev server to call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store: session_id -> ClaudeAgent (holds its own message history)
_sessions: dict[str, ClaudeAgent] = {}
_sessions_lock = Lock()


def _get_or_create_agent(session_id: str | None) -> tuple[str, ClaudeAgent]:
    if session_id and session_id in _sessions:
        return session_id, _sessions[session_id]

    new_id = session_id or str(uuid.uuid4())
    with _sessions_lock:
        agent = _sessions.setdefault(new_id, ClaudeAgent(tools=ALL_TOOLS))
    return new_id, agent


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    session_id, agent = _get_or_create_agent(request.session_id)

    try:
        reply = agent.chat(request.message)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return ChatResponse(session_id=session_id, response=reply)


@app.delete("/chat/{session_id}")
def end_session(session_id: str) -> dict:
    with _sessions_lock:
        existed = _sessions.pop(session_id, None) is not None

    if not existed:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted", "session_id": session_id}
