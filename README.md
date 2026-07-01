# Premium OTT Streaming Platform

A world-class premium OTT streaming platform inspired by Apple TV+, Netflix, Disney+, and Prime Video.

## Architecture

- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS + Framer Motion + Vidstack
  - Deployed on Vercel
  - Premium glassmorphism design with animated aurora background
  
- **Backend**: FastAPI + Telethon + MongoDB
  - Deployed on Hugging Face Docker Space
  - Telegram as media storage, MongoDB as metadata catalog
  - Chunked MTProto streaming with HTTP Range support

## Project Structure

```
ott-platform/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Config, security, logging
│   │   ├── database/     # MongoDB connection
│   │   ├── models/       # Data models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── telethon_exec/# Telegram integration
│   │   ├── workers/      # Background tasks
│   │   └── utils/        # Helpers
│   ├── Dockerfile
│   └── requirements.txt
│
└── frontend/         # Next.js frontend
    └── src/
        ├── app/          # App Router pages
        ├── components/   # UI components
        ├── lib/          # Utils, API client, constants
        ├── stores/       # Zustand stores
        ├── hooks/        # Custom hooks
        ├── services/     # API services
        └── types/        # TypeScript types
```

## Quick Start

### Backend
```bash
cd backend
cp .env.example .env  # Fill in credentials
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 7860 --reload
```

### Frontend
```bash
cd frontend
cp .env.example .env.local  # Set API URL
npm install
npm run dev
```

## License

Proprietary. All rights reserved.
