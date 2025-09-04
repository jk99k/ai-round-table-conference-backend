from pydantic import BaseModel
from ninja.orm import ModelSchema
from typing import Optional, List, Literal

from agents.schemas import AgentOutSchema
from .models import Debate, Message

class ModeratorResponse(BaseModel):
    statement: str
    reasoning: str
    conclusion_reason: Optional[Literal["NATURAL_CONCLUSION", "SUMMARY_PROVIDED", "STALEMATE"]]

class DebateCreateSchema(BaseModel):
    topic: str
    agent_ids: List[int]

class MessageOutSchema(ModelSchema):
    agent: AgentOutSchema = None
    class Config:
        model = Message
        model_fields = ["id", "turn", "content", "created_at"]

class DebateOutSchema(ModelSchema):
    messages: List[MessageOutSchema] = []
    class Config:
        model = Debate
        model_fields = "__all__"
