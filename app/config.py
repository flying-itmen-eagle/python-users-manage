# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 這裡的連線資訊會被 .env 檔案覆蓋（如果有 .env 的話）
    DATABASE_URL: str = "postgresql+psycopg2://users_manage:users_manage_pass@localhost/users_manage_system"

    class Config:
        env_file = ".env"

settings = Settings()
