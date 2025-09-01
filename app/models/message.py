"""
討論会メッセージテーブルのORMモデル。
"""

from typing import TYPE_CHECKING
from sqlalchemy import BIGINT, INTEGER, TEXT, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .debate import Debate
    from .agent import Agent


class Message(Base):
    """討論会メッセージテーブル。各発言ログ。"""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    debate_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("debates.id"), nullable=False
    )
    agent_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("agents.id"), nullable=False
    )
    content: Mapped[str] = mapped_column(TEXT, nullable=False)
    sequence_number: Mapped[int] = mapped_column(INTEGER, nullable=False)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    debate: Mapped["Debate"] = relationship("Debate", back_populates="messages")
    agent: Mapped["Agent"] = relationship("Agent", back_populates="messages")
