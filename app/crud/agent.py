from typing import List, Optional
from sqlalchemy.orm import Session
from models import Agent
from schemas.agent import AgentCreate

def create_agent(db: Session, agent: AgentCreate) -> Agent:
    db_agent = Agent(
        name=agent.name,
        persona_prompt=agent.persona_prompt,
        avatar_url=agent.avatar_url,
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def get_agent(db: Session, agent_id: int) -> Optional[Agent]:
    return db.query(Agent).filter(Agent.id == agent_id).first()

def get_agents(db: Session, skip: int = 0, limit: int = 100) -> List[Agent]:
    return db.query(Agent).offset(skip).limit(limit).all()
