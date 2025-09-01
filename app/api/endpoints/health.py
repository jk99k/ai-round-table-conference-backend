"""
ヘルスチェック用エンドポイント。
DB接続確認エンドポイントも含む。
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from sqlalchemy import text

router = APIRouter()

@router.get("/health", summary="ヘルスチェック")
def health_check():
    return {"status": "ok"}

@router.get("/db-health", summary="DBヘルスチェック")
def db_health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"db_status": "ok"}
    except Exception as e:
        return {"db_status": "ng", "detail": str(e)}
