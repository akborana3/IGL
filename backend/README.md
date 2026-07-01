---
title: IGL Backend
emoji: 🎬
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
---

# Premium OTT Streaming Platform — Backend

FastAPI backend that powers the premium OTT streaming platform. Uses Telegram as media storage, MongoDB as metadata catalog, and streams media directly from Telegram via MTProto.

## Tech Stack

- **FastAPI** — Web framework
- **Telethon** — Telegram MTProto client
- **MongoDB (Motor)** — Async metadata database
- **Pydantic** — Data validation
- **Uvicorn** — ASGI server

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your credentials
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `uvicorn app.main:app --host 0.0.0.0 --port 7860 --reload`

## Environment Variables

| Variable | Description |
|----------|-------------|
| `API_ID` | Telegram API ID |
| `API_HASH` | Telegram API Hash |
| `SESSION_STRING` | Telethon string session |
| `CHANNEL_ID` | Private Telegram channel ID |
| `MONGO_URL` | MongoDB connection URL |
| `MONGO_DB` | MongoDB database name |
| `ADMIN_USERNAME` | Admin username |
| `ADMIN_PASSWORD_HASH` | Bcrypt hash of admin password |
| `SECRET_KEY` | JWT secret key |
| `CORS_ORIGINS` | Comma-separated allowed origins |
| `SYNC_INTERVAL_SECONDS` | Background sync interval |

## API Endpoints

### Public
- `GET /api/home` — All homepage data
- `GET /api/trending` — Trending media
- `GET /api/latest` — Recently added media
- `GET /api/categories` — All categories
- `GET /api/media/{slug}` — Media detail
- `GET /api/related/{slug}` — Related media
- `GET /api/search` — Search with filters
- `GET /api/stream/{message_id}` — Stream media (HTTP Range support)
- `GET /api/download/{message_id}` — Download media (HTTP Range support)

### Admin (JWT required)
- `POST /api/admin/login` — Admin login
- `GET /api/admin/dashboard` — Dashboard summary
- `POST /api/admin/media/update` — Update metadata
- `POST /api/admin/media/feature` — Feature/unfeature media
- `POST /api/admin/media/delete` — Delete metadata
- `POST /api/admin/sync` — Trigger manual sync
- `GET /api/admin/analytics` — Analytics data

## Deployment

Deploy on Hugging Face Docker Space. The Dockerfile is included.

## Architecture

- Telegram = media storage (never downloaded to disk)
- MongoDB = metadata catalog
- FastAPI = API + streaming gateway
- Streaming = chunked MTProto → StreamingResponse with HTTP Range support
