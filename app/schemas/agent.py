from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class AgentBase(BaseModel):
    name: str
    persona_prompt: str
    avatar_url: Optional[str] = None

class AgentCreate(AgentBase):
    pass

class AgentRead(AgentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
