"""
ヘルスチェック用エンドポイント。
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", summary="ヘルスチェック")
def health_check():
    return {"status": "ok"}
