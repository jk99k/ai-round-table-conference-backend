from pydantic import BaseModel
from ninja.orm import ModelSchema
from typing import Optional, List, Literal

from agents.schemas import AgentOutSchema
from .models import Debate, Message

class InterruptDebateIn(BaseModel):
    content: str

class ModeratorResponse(BaseModel):
    statement: str
    reasoning: str
    conclusion_reason: Optional[Literal["NATURAL_CONCLUSION", "SUMMARY_PROVIDED", "STALEMATE"]]
    agent_id: Optional[int] = None  # ← 追加
    agent_name: Optional[str] = None  # ← 追加

class DebateCreateSchema(BaseModel):
    topic: str
    agent_ids: List[int]

class MessageOutSchema(ModelSchema):
    agent: Optional[AgentOutSchema] = None
    class Config:
        model = Message
        model_fields = ["id", "turn", "content", "created_at"]

class DebateOutSchema(ModelSchema):
    messages: List[MessageOutSchema] = []
    agents: List[AgentOutSchema] = []
    next_agent_id: Optional[int] = None
    next_agent_name: Optional[str] = None
    class Config:
        model = Debate
        model_fields = "__all__"

class DebateDeleteIn(BaseModel):
    ids: list[int]