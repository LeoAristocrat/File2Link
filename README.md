# File2Link

File2Link is a FastAPI service that turns Telegram-stored media into secure stream and download links.

## Use case

Useful when a bot stores files in a Telegram channel and you want to expose those files through controlled web URLs.

## Features

- Signed URL tokens with expiry
- Stream endpoint for browser playback
- Direct download endpoint with range support
- Telethon-based Telegram integration
- Health check endpoint

## Requirements

- Python 3.11+
- Telegram `API_ID` and `API_HASH`
- Bot token and log channel ID

## Setup

```bash
git clone https://github.com/LeoAristocrat/File2Link.git
cd File2Link
pip install -r requirements.txt
cp .env.example .env
```

Then fill in `.env` and start the API with your preferred ASGI runner.
