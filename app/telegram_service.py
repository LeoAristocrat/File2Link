from __future__ import annotations

from dataclasses import dataclass
from mimetypes import guess_type

from telethon import TelegramClient


@dataclass
class TelegramFile:
    filename: str
    mime_type: str
    content: bytes


class TelegramFileService:
    def __init__(self, client: TelegramClient, log_channel_id: int):
        self.client = client
        self.log_channel_id = log_channel_id

    async def fetch_file(self, file_id: int) -> TelegramFile:
        message = await self.client.get_messages(self.log_channel_id, ids=file_id)
        if not message or not message.media:
            raise FileNotFoundError("Message or media not found")

        filename = getattr(getattr(message, "file", None), "name", None) or f"media_{file_id}"
        mime_type = getattr(getattr(message, "file", None), "mime_type", None) or guess_type(filename)[0] or "application/octet-stream"
        data = await self.client.download_media(message, file=bytes)
        if not data:
            raise FileNotFoundError("Media content is empty")

        return TelegramFile(filename=filename, mime_type=mime_type, content=data)
