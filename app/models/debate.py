"""
討論会テーブルのORMモデル。
"""

from sqlalchemy import BIGINT, VARCHAR, TEXT, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message
    from .user import User
    from .agent import Agent


class Debate(Base):
    """討論会テーブル。ユーザーが作成し、複数エージェントが参加。"""

    __tablename__ = "debates"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id"))
    theme: Mapped[str] = mapped_column(TEXT, nullable=False)
    status: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="debate")
    user: Mapped["User"] = relationship("User", back_populates="debates")
    agents: Mapped[list["Agent"]] = relationship(
        "Agent", secondary="debate_participants", back_populates="debates"
    )
