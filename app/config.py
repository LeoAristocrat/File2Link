from dotenv import load_dotenv

load_dotenv()

import os
from dataclasses import dataclass


def _env_int(name: str, default: int | None = None) -> int | None:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Leo File2Link")
    api_id: int | None = _env_int("API_ID")
    api_hash: str | None = os.getenv("API_HASH")
    bot_token: str | None = os.getenv("BOT_TOKEN")
    log_channel_id: int | None = _env_int("LOG_CHANNEL_ID")
    session_name: str = os.getenv("SESSION_NAME", "leo_file2link")
    auth_secret: str = os.getenv("AUTH_SECRET", "change-me-now")
    token_ttl_seconds: int = _env_int("TOKEN_TTL_SECONDS", 3600) or 3600
    admin_key: str = os.getenv("ADMIN_KEY", "")


settings = Settings()
