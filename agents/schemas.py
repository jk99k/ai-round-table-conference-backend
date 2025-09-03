from ninja import ModelSchema
from .models import Agent
from pydantic import BaseModel

class AgentCreateSchema(BaseModel):
    name: str

class AgentOutSchema(ModelSchema):
    class Config:
        model = Agent
        model_fields = "__all__"
