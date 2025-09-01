"""
FastAPIアプリのエントリーポイント。CORS設定とルーター登録を行う。
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import health, debate

app = FastAPI(title="Brainstorming Colosseum API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(health.router, prefix="/api/v1")
app.include_router(debate.router, prefix="/api/v1/debates")
