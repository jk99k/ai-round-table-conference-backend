"""
環境変数・設定管理。Pydantic BaseSettingsを利用。
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()
