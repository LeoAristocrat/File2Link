from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.http_utils import parse_range_header
from app.security import sign_token, verify_token
from app.telegram_service import TelegramFileService


def build_router(templates: Jinja2Templates, file_service: TelegramFileService) -> APIRouter:
    router = APIRouter()

    @router.get("/", response_class=HTMLResponse)
    async def home(request: Request):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "app_name": settings.app_name,
            },
        )

    @router.get("/health")
    async def health():
        return {"status": "ok", "app": settings.app_name}

    @router.get("/token/{file_id}")
    async def create_token(file_id: int, ttl: int = Query(default=settings.token_ttl_seconds), admin_key: str = Query(default="")):
        if settings.admin_key and admin_key != settings.admin_key:
            raise HTTPException(status_code=403, detail="Invalid admin key")
        token = sign_token(file_id=file_id, ttl_seconds=ttl, secret=settings.auth_secret)
        return {"file_id": file_id, "token": token, "expires_in": ttl}

    @router.get("/stream/{file_id}", response_class=HTMLResponse)
    async def stream_page(request: Request, file_id: int, token: str = Query(...)):
        if not verify_token(token=token, expected_file_id=file_id, secret=settings.auth_secret):
            raise HTTPException(status_code=403, detail="Invalid or expired token")
        return templates.TemplateResponse(
            "player.html",
            {
                "request": request,
                "file_id": file_id,
                "token": token,
                "download_url": f"/dl/{file_id}?token={token}",
            },
        )

    @router.get("/dl/{file_id}")
    async def download_file(file_id: int, token: str = Query(...), range_header: str | None = Header(default=None, alias="Range")):
        if not verify_token(token=token, expected_file_id=file_id, secret=settings.auth_secret):
            raise HTTPException(status_code=403, detail="Invalid or expired token")

        try:
            telegram_file = await file_service.fetch_file(file_id)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail="Unable to retrieve media") from exc

        total = len(telegram_file.content)
        try:
            start, end, partial = parse_range_header(range_header, total)
        except ValueError as exc:
            raise HTTPException(status_code=416, detail=str(exc)) from exc

        payload = telegram_file.content[start : end + 1]
        headers = {
            "Accept-Ranges": "bytes",
            "Content-Disposition": f'inline; filename="{telegram_file.filename}"',
            "Content-Length": str(len(payload)),
        }
        if partial:
            headers["Content-Range"] = f"bytes {start}-{end}/{total}"
            status_code = 206
        else:
            status_code = 200

        return Response(content=payload, media_type=telegram_file.mime_type, headers=headers, status_code=status_code)

    return router
