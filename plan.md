# plan.md
Premium OTT Streaming Platform — Frontend Specification

Project Overview

Build a world-class premium OTT streaming platform inspired by Apple TV+, Netflix, Disney+, and Prime Video.

The goal is to create a website that feels expensive, cinematic, smooth, elegant, and modern rather than looking like a typical media website.

Every interaction should feel polished with premium animations, realistic glassmorphism, smooth transitions, subtle 3D depth, and excellent performance.

The frontend must be production-ready and fully responsive.

The frontend will be deployed on Vercel.

The frontend communicates only with the FastAPI backend through REST APIs. It must never access Telegram directly.

---

Technology Stack

Use:

- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- Framer Motion
- GSAP
- React Three Fiber
- Drei
- Vidstack Player
- Lucide Icons
- Zustand for client state
- React Hook Form
- Zod
- Axios
- Motion One where appropriate

Use Server Components whenever possible.

Only use Client Components where interactivity is required.

Follow the latest Next.js best practices.

---

Design Language

The website must feel like a premium OTT service.

Visual style:

- Dark luxury interface
- Frosted Glass UI
- Glassmorphism
- Large cinematic banners
- Aurora gradient backgrounds
- Premium shadows
- Neon purple + blue accent colors
- Smooth glow effects
- Rounded corners
- Floating cards
- Premium hover animations
- Soft blur
- Rich spacing
- Beautiful typography
- Excellent readability

Never use flat or boring layouts.

Every page should feel alive.

---

Background Effects

The background should never be static.

Include:

Animated Aurora

React Three Fiber background

Floating particles

Animated gradient meshes

Blurred glowing orbs

Mouse parallax

Subtle depth

Everything must remain lightweight.

---

Motion Design

Animations should feel similar to Apple TV+.

Use:

Framer Motion page transitions

Smooth fade animations

Hero image zoom

Glass hover effects

Card scaling

3D tilt

Magnetic buttons

Animated navigation

Scroll reveal

Smooth loading animations

Skeleton loading

Animated search

Page transition effects

No sudden animation.

Everything should be smooth.

---

Responsive Design

Support:

Desktop

Laptop

Tablet

Mobile

Landscape devices

Cards should automatically resize.

Navigation should adapt automatically.

Player should be responsive.

No horizontal scrolling.

---

Navigation

Top Navigation

Logo

Browse

Categories

Search

About

Contact

Desktop Navigation

Glass navigation bar

Sticky

Transparent while at top

Blur when scrolling

Shrink on scroll

Mobile Navigation

Animated bottom navigation

Hamburger drawer

Smooth opening animation

---

Homepage

The homepage should immediately impress users.

Sections:

Large Cinematic Hero Banner

Featured Content

Trending This Week

Continue Watching

Recently Added

Most Popular

Top Rated

Categories

Collections

Latest Uploads

Footer

Every section should load independently.

Cards should animate into view.

---

Hero Banner

Large cinematic background.

Auto rotating.

Glass information panel.

Display:

Title

Description

Runtime

Genres

Release Year

Watch Now button

More Info button

Animated background.

Subtle zoom effect.

Gradient overlays.

---

Browse Page

Infinite scrolling.

Grid layout.

Category filters.

Sorting.

Search.

Animated loading.

Responsive cards.

---

Search

Instant search.

Debounced requests.

Highlight matching text.

Suggestions while typing.

Filters:

Category

Genre

Year

Duration

Sort:

Newest

Oldest

Most Viewed

Most Downloaded

Alphabetical

---

Categories

Beautiful category cards.

Each category has:

Large background

Icon

Media count

Hover animation

Opening animation

---

Media Detail Page

Large cinematic header.

Glass information panel.

Display:

Poster

Title

Description

Duration

Resolution

Genres

Upload Date

Views

Downloads

Tags

Related Media

Watch Button

Download Button

Share Button

Favorite Button

Smooth scrolling.

Sticky player.

---

Video Player

Use Vidstack Player.

Features:

Adaptive layout

Theater Mode

Fullscreen

Picture-in-Picture

Subtitle support

Audio tracks

Keyboard shortcuts

Playback speed

Volume controls

Seek controls

Double-tap gestures on mobile

Resume playback

Watch progress indicator

Modern controls

Glass UI

Auto-hide controls

---

Episode Cards

Large thumbnail

Glass overlay

Animated hover

3D tilt

Runtime badge

Category badge

View count

Download count

Share button

Favorite button

Lazy loaded images

Progress indicator

---

Continue Watching

Store locally in browser.

Remember:

Playback progress

Last watched position

Recently watched

Continue Watching appears automatically.

---

Favorites

No login required.

Store locally.

Allow:

Add

Remove

Quick access

Animated favorite icon.

---

Watch History

No login required.

Store locally.

Display:

Recently watched

Playback progress

Continue watching

Clear history option.

---

Loading Experience

Every page should have:

Beautiful skeletons

Progress bars

Image placeholders

Smooth fade in

Progressive loading

Blur-up images

Never display blank screens.

---

Performance

Use:

Image optimization

Code splitting

Dynamic imports

Lazy loading

Prefetching

Server Components

Streaming rendering

Route caching

Optimized fonts

Bundle optimization

---

Accessibility

Keyboard navigation.

ARIA labels.

Focus indicators.

High contrast.

Reduced motion support.

Screen reader friendly.

---

SEO

Generate:

Metadata

OpenGraph

Twitter cards

JSON-LD

Sitemap

robots.txt

Canonical URLs

Dynamic titles

Dynamic descriptions

---

Error Pages

Beautiful:

404

500

Offline

Loading

Empty State

Each page should follow the same premium design language.

---

Theme

Default theme is dark.

Support optional light mode.

Remember user preference.

---

API Integration

All data comes from the FastAPI backend.

Never connect directly to Telegram.

Use REST APIs.

Implement:

Request retry

Timeouts

Loading states

Error handling

Optimistic UI

Caching

---

Folder Structure

Follow a clean architecture.

Separate:

Components

Layouts

Animations

Hooks

Utilities

Types

Services

Stores

Contexts

Pages

Providers

Styles

Icons

Keep components reusable.

Avoid duplicate code.

---

Coding Standards

Use strict TypeScript.

Reusable components only.

No inline styles.

No duplicated logic.

Use environment variables.

Write clean code.

Comment complex logic.

Follow scalable architecture.

The frontend should be production-ready, optimized for Vercel deployment, and deliver a premium OTT experience with cinematic visuals, elegant animations, responsive layouts, and seamless integration with the FastAPI backend.


#BACKEND plan.md
Premium OTT Streaming Platform — Backend Specification

Project Overview

Build a production-grade backend that powers the premium OTT streaming website.

The backend will be deployed on Hugging Face Spaces (Docker SDK) and expose REST APIs consumed by the Next.js frontend hosted on Vercel.

The backend is responsible for:

- Telegram media indexing
- Media streaming
- Download handling
- Metadata management
- Search
- Admin dashboard
- Analytics
- Background synchronization
- Thumbnail management
- Media organization

The backend should never permanently store media files. Telegram is the storage backend.

---

Technology Stack

Use:

- FastAPI
- Python 3.12+
- Telethon (MTProto)
- MongoDB
- Motor (Async MongoDB)
- Uvicorn
- Pydantic
- aiofiles (only for temporary files if required)
- Pillow (thumbnail processing if needed)
- FFmpeg (metadata extraction if required)

Everything must be asynchronous.

---

Deployment

Deploy on Hugging Face Docker Space.

The repository should include:

- Dockerfile
- requirements.txt
- .dockerignore
- .env.example
- startup script

The container should automatically start FastAPI.

Store configuration using environment variables.

---

Database

Use MongoDB only.

Collections:

- media
- categories
- homepage
- analytics
- admin
- settings

---

Media Collection

Each indexed Telegram message becomes one MongoDB document.

Example fields:

- telegram_message_id
- channel_id
- title
- description
- caption
- slug
- category
- tags
- duration
- width
- height
- file_size
- mime_type
- thumbnail
- upload_date
- views
- downloads
- featured
- created_at
- updated_at

Never store the actual media file.

---

Telegram Architecture

Telegram is the permanent storage.

Media remains inside the private Telegram channel.

MongoDB stores only metadata.

Frontend never communicates with Telegram.

Only FastAPI communicates with Telegram through Telethon.

---

Telethon Session

The backend uses:

- API_ID
- API_HASH
- String Session
- Private Channel ID

The provided bot tokens may be used for bot-specific tasks if needed, but all media access should be performed using the Telethon user session because MTProto provides full media access.

---

Media Indexing

Create a dedicated module:

telethon_exec/

Responsibilities:

- connect to Telegram
- scan channel history
- detect new uploads
- update MongoDB
- retrieve metadata
- stream media
- download media

---

Initial Scan

During first startup:

Connect using Telethon.

Iterate through every message in the private channel.

If the message contains:

- Video
- Audio
- Movie
- Document

Extract:

Message ID

Caption

Duration

Resolution

Filename

MIME Type

File Size

Thumbnail

Upload Date

Generate:

Title

Slug

Category

Tags

Store all metadata inside MongoDB.

Skip duplicate entries using the Telegram Message ID.

---

Continuous Synchronization

Run a background synchronization task.

Every synchronization cycle:

- Read newly added messages.
- Compare with MongoDB.
- Insert missing media.
- Update edited captions.
- Ignore duplicates.
- Remove records only if explicitly configured.

Synchronization should happen automatically without restarting the server.

---

Streaming Architecture

Streaming must happen directly from Telegram.

The server should never download an entire media file before playback.

Workflow:

1. User presses Play.
2. Frontend requests "/api/stream/{message_id}".
3. FastAPI retrieves the media document from MongoDB.
4. Using the stored Telegram Message ID, Telethon loads the corresponding Telegram message.
5. Telethon opens an MTProto download stream and reads the file incrementally in chunks.
6. FastAPI wraps those chunks in an asynchronous generator and returns them with "StreamingResponse".
7. Each chunk is sent to the browser immediately as it is received.
8. The complete file is never stored on disk.

Streaming begins within seconds because data is forwarded while it is being read from Telegram.

---

HTTP Range Support

The streaming endpoint must support browser seeking.

When the browser sends:

Range: bytes=start-end

The backend should:

- Parse the requested byte range.
- Calculate the correct Telegram file offset.
- Start reading from that offset through Telethon.
- Stream only the requested bytes.
- Return HTTP 206 Partial Content with appropriate headers.

This enables:

- Instant seeking
- Resume playback
- Jump forward/backward
- Browser compatibility

---

Chunked MTProto Reading

Media should be transferred chunk-by-chunk.

Example flow:

- Browser requests bytes.
- FastAPI requests matching chunks from Telegram.
- Telegram returns encrypted MTProto chunks.
- Telethon decrypts them.
- FastAPI immediately forwards the bytes to the client.

No intermediate file should be created unless a temporary buffer is absolutely necessary.

Memory usage should remain low even for very large files.

---

Download Architecture

When the user clicks Download:

1. Frontend requests "/api/download/{message_id}".
2. FastAPI finds the MongoDB record.
3. Telethon reads the Telegram file in chunks.
4. FastAPI streams those chunks as a downloadable response.
5. After a successful transfer, increment the download counter in MongoDB.

Support resumable downloads using HTTP Range requests.

---

Views & Analytics

Whenever playback starts:

Increment:

- total views
- daily views
- media views

Whenever a download completes:

Increment:

- total downloads
- daily downloads
- media downloads

Store timestamps for analytics.

---

Search

Provide APIs for:

- search
- latest
- trending
- popular
- featured
- categories
- related media

Search by:

- title
- slug
- description
- caption
- tags
- category

Support pagination and sorting.

---

Homepage APIs

Create endpoints for:

- Hero Banner
- Trending
- Recently Added
- Continue Watching (frontend-managed)
- Featured Collections
- Categories
- Popular
- Latest Uploads

---

Thumbnail Handling

If Telegram already provides thumbnails:

Store the thumbnail reference.

If needed, generate a resized thumbnail temporarily and cache only the thumbnail, not the original media.

---

Admin Dashboard

Only the admin panel requires authentication.

Visitors do not need accounts.

Admin features:

- Secure login
- Manage homepage sections
- Edit metadata
- Change titles
- Update descriptions
- Manage categories
- Feature or unfeature media
- Delete metadata records (without deleting Telegram media unless explicitly requested)
- Trigger manual synchronization
- View analytics
- Monitor backend status

---

Background Workers

Run asynchronous background tasks for:

- Telegram synchronization
- Analytics aggregation
- Thumbnail processing
- Cleanup of temporary files
- Health monitoring

These tasks must not block API requests.

---

Security

Implement:

- HTTPS support
- CORS configuration for the Vercel frontend
- Admin authentication
- Secure password hashing
- Input validation
- Rate limiting for sensitive endpoints
- Audit logging for admin actions
- Environment variable management
- Secret isolation

---

API Structure

Suggested endpoints:

GET /api/home

GET /api/trending

GET /api/latest

GET /api/categories

GET /api/media/{slug}

GET /api/search

GET /api/stream/{message_id}

GET /api/download/{message_id}

GET /api/related/{message_id}

POST /api/admin/login

GET /api/admin/dashboard

POST /api/admin/media/update

POST /api/admin/media/feature

POST /api/admin/sync

GET /api/admin/analytics

---

Folder Structure

backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── telethon_exec/
│   ├── workers/
│   ├── utils/
│   └── main.py
│
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md

Keep all Telegram-specific logic isolated inside "telethon_exec".

---

Error Handling

Gracefully handle:

- FloodWait errors
- Network interruptions
- Missing Telegram messages
- Corrupted metadata
- Invalid range requests
- MongoDB connection failures

Automatically retry transient Telegram operations where appropriate.

---

Performance

The backend should:

- Use asynchronous I/O throughout.
- Stream data instead of buffering entire files.
- Avoid unnecessary memory usage.
- Paginate large result sets.
- Create indexes on frequently queried MongoDB fields.
- Keep API responses lightweight.

---

Code Quality

Write production-ready, modular, and well-documented code.

Requirements:

- Strict type hints
- Reusable services
- Clear separation of concerns
- Comprehensive logging
- Environment-based configuration
- Clean error messages
- Consistent naming
- Easy extensibility

The final backend should provide a scalable streaming service where Telegram functions as the media storage layer, MongoDB serves as the searchable metadata catalogue, FastAPI acts as the API and streaming gateway, and the Next.js frontend delivers the premium OTT user experience.
