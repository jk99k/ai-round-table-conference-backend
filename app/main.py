"""
FastAPIアプリのエントリーポイント。CORS設定とルーター登録を行う。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import health, debate, agent

app = FastAPI(title="AI円卓会議API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(health.router, prefix="/v1")
app.include_router(debate.router, prefix="/v1/debates")
app.include_router(agent.router, prefix="/v1/agents", tags=["agents"])
