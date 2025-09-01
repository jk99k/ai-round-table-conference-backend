"""
Brainstorming Colosseum DBモデル定義（SQLAlchemy 2.0同期スタイル）
各テーブルのORMクラスとリレーションシップをまとめて記述。
"""

from sqlalchemy import BIGINT, INTEGER, TEXT, VARCHAR, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

# 全モデルのベースクラス
Base = declarative_base()


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

    # 1ユーザーが複数の討論会を持つ
    debates: Mapped[list["Debate"]] = relationship("Debate", back_populates="user")


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

    # 1エージェントが複数のメッセージを持つ
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="agent")
    # 多対多: 参加討論会
    debates: Mapped[list["Debate"]] = relationship(
        "Debate", secondary="debate_participants", back_populates="agents"
    )


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

    # 1討論会が複数のメッセージを持つ
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="debate")
    # 作成ユーザー
    user: Mapped["User"] = relationship("User", back_populates="debates")
    # 多対多: 参加エージェント
    agents: Mapped[list["Agent"]] = relationship(
        "Agent", secondary="debate_participants", back_populates="debates"
    )


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

    # メッセージの討論会
    debate: Mapped["Debate"] = relationship("Debate", back_populates="messages")
    # メッセージのエージェント
    agent: Mapped["Agent"] = relationship("Agent", back_populates="messages")
