from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas.agent import AgentCreate, AgentRead
from crud.agent import create_agent, get_agent, get_agents
from db.session import get_db

router = APIRouter(
)

@router.post("", response_model=AgentRead)
def create_agent_endpoint(agent: AgentCreate, db: Session = Depends(get_db)):
    return create_agent(db, agent)

@router.get("", response_model=List[AgentRead])
def read_agents_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_agents(db, skip=skip, limit=limit)

@router.get("/{agent_id}", response_model=AgentRead)
def read_agent_endpoint(agent_id: int, db: Session = Depends(get_db)):
    db_agent = get_agent(db, agent_id)
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return db_agent
