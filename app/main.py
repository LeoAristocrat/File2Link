from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from telethon import TelegramClient

from app.config import settings
from app.routes.files import build_router
from app.telegram_service import TelegramFileService


def _build_client() -> TelegramClient:
    if settings.api_id is None or settings.api_hash is None or settings.bot_token is None:
        raise RuntimeError("API_ID, API_HASH, and BOT_TOKEN are required")
    return TelegramClient(settings.session_name, settings.api_id, settings.api_hash)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = _build_client()
    await client.start(bot_token=settings.bot_token)

    if settings.log_channel_id is None:
        raise RuntimeError("LOG_CHANNEL_ID is required")

    templates = Jinja2Templates(directory="templates")
    file_service = TelegramFileService(client=client, log_channel_id=settings.log_channel_id)
    app.include_router(build_router(templates=templates, file_service=file_service))

    yield

    await client.disconnect()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
