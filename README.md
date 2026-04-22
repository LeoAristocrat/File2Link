# File2Link
![File2Link Banner](https://i.ibb.co/7tKcTg7K/Chat-GPT-Image-Apr-13-2026-11-18-07-AM.png)

File2Link is a FastAPI service that converts Telegram-stored media into secure stream and direct-download links.

It is designed for bots and automation workflows where files are saved in a Telegram log channel and then served through web URLs with token-based access control.

## Features

- Signed, expiring access tokens
- Stream page endpoint for browser playback
- Direct download endpoint with HTTP range support
- Telegram integration through Telethon
- Health check endpoint for uptime monitoring

## Requirements

- Python 3.11+
- Telegram `API_ID` and `API_HASH`
- Telegram bot token
- Telegram log channel ID

## Installation

```bash
git clone https://github.com/LeoAristocrat/File2Link.git
cd File2Link
pip install -r requirements.txt
```

Copy the example environment file and update values:

```bash
cp .env.example .env
```

## Configuration

Set these values in `.env`:

- `APP_NAME` - Display name shown by the API
- `API_ID` - Telegram API ID
- `API_HASH` - Telegram API hash
- `BOT_TOKEN` - Bot token from BotFather
- `LOG_CHANNEL_ID` - Channel ID where source files are stored
- `SESSION_NAME` - Telethon session name
- `AUTH_SECRET` - Secret used to sign tokens
- `TOKEN_TTL_SECONDS` - Default token lifetime (seconds)
- `ADMIN_KEY` - Optional key required to create tokens

## Run

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - Homepage
- `GET /health` - Health status
- `GET /token/{file_id}` - Generate signed token
- `GET /stream/{file_id}` - Render player page
- `GET /dl/{file_id}` - Download or stream file bytes

## Basic Flow

1. Request a token for a Telegram message ID.
2. Open `/stream/{file_id}?token=...` for browser playback.
3. Use `/dl/{file_id}?token=...` for direct file delivery.

## Example Requests

Create token:

```bash
curl "http://localhost:8000/token/12345?admin_key=YOUR_ADMIN_KEY"
```

Open stream page:

```bash
curl "http://localhost:8000/stream/12345?token=YOUR_TOKEN"
```

Download with range:

```bash
curl -H "Range: bytes=0-1048575" "http://localhost:8000/dl/12345?token=YOUR_TOKEN"
```

## License

MIT
