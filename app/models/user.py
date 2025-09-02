"""
ユーザーテーブルのORMモデル。
"""

from sqlalchemy import BIGINT, VARCHAR, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .debate import Debate

class User(Base):
    """ユーザー情報テーブル。1ユーザーは複数の討論会を持つ。"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    debates: Mapped[list["Debate"]] = relationship("Debate", back_populates="user")
