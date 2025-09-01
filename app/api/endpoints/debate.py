"""
討論会（debates）CRUD用エンドポイントの雛形。
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
# from app.models.debate import Debate
# from app.schemas.debate import DebateCreate, DebateRead

router = APIRouter()

@router.post("/", summary="討論会作成")
def create_debate():
    # 実装は後ほど
    return {"message": "Not implemented"}

@router.get("/{debate_id}", summary="討論会取得")
def get_debate(debate_id: int):
    # 実装は後ほど
    return {"message": "Not implemented"}

@router.get("/", summary="討論会一覧")
def list_debates():
    # 実装は後ほど
    return []
