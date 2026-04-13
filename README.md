# File2Link Clean

A fresh implementation of a Telegram media link service with the same core behavior and a new architecture.

## What is different

- New modular codebase under `app/`
- Signed expiring token system using HMAC-SHA256
- Built-in `/health` endpoint
- Simpler maintainable templates

## Core behavior preserved

- Fetch media from a Telegram log channel by message ID
- Stream using browser-compatible player endpoint
- Download with HTTP range support

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill values.
4. Run server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Token workflow

1. Generate token:

```bash
GET /token/{file_id}?admin_key=YOUR_ADMIN_KEY
```

2. Stream:

```bash
GET /stream/{file_id}?token=TOKEN
```

3. Download:

```bash
GET /dl/{file_id}?token=TOKEN
```

## Notes

- `API_ID`, `API_HASH`, `BOT_TOKEN`, and `LOG_CHANNEL_ID` are required.
- Set a strong `AUTH_SECRET` in production.
