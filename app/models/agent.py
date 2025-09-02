"""
AIエージェントテーブルのORMモデル。
"""

from sqlalchemy import BIGINT, VARCHAR, TEXT, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message
    from .debate import Debate


class Agent(Base):
    """AIエージェント情報テーブル。討論参加者。"""

    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    persona_prompt: Mapped[str] = mapped_column(TEXT, nullable=False)
    avatar_url: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="agent")
    debates: Mapped[list["Debate"]] = relationship(
        "Debate", secondary="debate_participants", back_populates="agents"
    )
