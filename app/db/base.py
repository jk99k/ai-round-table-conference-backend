"""
SQLAlchemyモデルのBaseクラス定義。Alembic連携用。
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Alembicの自動検出用: models配下の全モデルをimport
from models import *
