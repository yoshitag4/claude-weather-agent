from typing import Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message to send to the agent")
    session_id: Optional[str] = Field(
        None, description="Conversation session id. Omit to start a new session."
    )


class ChatResponse(BaseModel):
    session_id: str
    response: str


class HealthResponse(BaseModel):
    status: str = "ok"
