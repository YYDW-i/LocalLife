from __future__ import annotations

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_data_dir() -> Path:
    # Windows: %LOCALAPPDATA%\LocalLife
    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        return Path(local_appdata) / "LocalLife"
    # Fallback (Linux/macOS): ~/.locallife
    return Path.home() / ".locallife"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "LocalLife"
    API_PREFIX: str = "/api"

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    DATA_DIR: Path = _default_data_dir()
    DB_FILE: str = "locallife.db"

    # 逗号分隔，如: http://127.0.0.1:5173,http://localhost:5173
    CORS_ORIGINS: str = "http://127.0.0.1:5173,http://localhost:5173"

    # Scheduler
    SCHEDULER_ENABLED: bool = True

    @property
    def db_path(self) -> Path:
        return self.DATA_DIR / self.DB_FILE


settings = Settings()
