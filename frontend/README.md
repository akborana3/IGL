# Premium OTT Streaming Platform — Frontend

A world-class premium OTT streaming platform built with Next.js 15, featuring cinematic visuals, glassmorphism design, and smooth animations.

## Tech Stack

- **Next.js 15** (App Router) — Framework
- **TypeScript** — Type safety
- **Tailwind CSS** — Styling
- **Framer Motion** — Animations
- **React Three Fiber** — 3D background effects
- **Vidstack** — Video player
- **Zustand** — State management (favorites, watch history)
- **Axios** — API client

## Getting Started

1. Install dependencies: `npm install`
2. Copy `.env.example` to `.env.local` and set your API URL
3. Run dev server: `npm run dev`
4. Open `http://localhost:3000`

## Environment Variables

| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | FastAPI backend URL |

## Pages

- `/` — Homepage with hero banner, trending, categories, and more
- `/browse` — Browse with infinite scroll, filters, and sorting
- `/search` — Instant debounced search with filters
- `/categories` — Beautiful category cards
- `/media/[slug]` — Media detail with related content
- `/player/[slug]` — Video player with resume playback

## Features

- Dark luxury glassmorphism design
- Animated aurora 3D background
- Premium animations (page transitions, scroll reveal, 3D tilt, magnetic buttons)
- Favorites (localStorage, no login)
- Watch history & continue watching (localStorage)
- Skeleton loading states
- SEO optimized (OpenGraph, Twitter cards, sitemap, robots)
- Fully responsive (desktop, tablet, mobile)
- Accessibility (keyboard nav, ARIA, reduced motion)

## Deployment

Deploy on Vercel. Set `NEXT_PUBLIC_API_URL` to your backend URL.
