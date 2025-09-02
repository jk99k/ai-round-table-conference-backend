"""
討論会参加者（中間）テーブルのORMモデル。
"""

from sqlalchemy import BIGINT, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from db.base import Base


class DebateParticipant(Base):
    """討論会参加者テーブル。討論会とエージェントの多対多中間テーブル。"""

    __tablename__ = "debate_participants"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    debate_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("debates.id"), nullable=False
    )
    agent_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey("agents.id"), nullable=False
    )
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
