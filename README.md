<div align="center">

# ☕ Chai Sutta

**AI-powered hyperlocal city intelligence platform**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+PostGIS-blue?logo=postgresql)](https://postgis.net/)
[![Redis](https://img.shields.io/badge/Redis-7-red?logo=redis)](https://redis.io/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-purple)](https://qdrant.tech/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?logo=docker)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*Real-time news · Weather · Traffic · Train status · Community reports · AI city assistant*

</div>

---

## 📖 Overview

**Chai Sutta** is a hyperlocal city intelligence backend that aggregates and serves real-time data about Indian cities — news feeds, live weather, traffic incidents, train statuses, community-filed reports, and trending topics — all powered by LLMs for natural-language city insights.

The name is a nod to the quintessential Indian street corner (the *chai-sutta* spot) where local news and gossip flows freely. The platform replicates that for the digital age...

### Core Capabilities

| Feature | Description |
|---|---|
| 🗞️ **Hyperlocal News** | City/zone-level news ingested from RSS feeds + web scraping |
| 🌦️ **Live Weather** | Real-time conditions and forecasts |
| 🚦 **Traffic Intelligence** | Incident reports and congestion via TomTom API |
| 🚂 **Train Status** | Live train running status for Indian Railways |
| 📣 **Community Reports** | User-filed geo-tagged incident reports with voting |
| 🔍 **Semantic Search** | Vector-powered content search via Qdrant |
| 🤖 **Ask Tapri** | LLM city assistant powered by Gemini / Groq |
| 📊 **City Mood & Summary** | AI-generated daily city snapshots |
| 📈 **Trending Topics** | Surfacing what the city is buzzing about |

---

## 🏗️ Architecture

```
chai-sutta/
├── app/
│   ├── main.py               # FastAPI app factory & lifespan management
│   ├── config.py             # Pydantic-settings configuration
│   ├── api/
│   │   ├── deps.py           # Shared FastAPI dependencies
│   │   └── v1/               # REST API endpoints (v1)
│   │       ├── auth.py       # JWT + Google OAuth
│   │       ├── news.py       # News feed endpoints
│   │       ├── weather.py    # Weather endpoints
│   │       ├── traffic.py    # Traffic endpoints
│   │       ├── trains.py     # Train status endpoints
│   │       ├── events.py     # City events endpoints
│   │       ├── reports.py    # Community reports + voting
│   │       ├── trending.py   # Trending topics
│   │       ├── city_mood.py  # City mood scoring
│   │       ├── city_summary.py # AI city summary
│   │       ├── chat.py       # Ask Tapri AI chat
│   │       ├── search.py     # Semantic search
│   │       └── profile.py    # User profile management
│   ├── core/
│   │   ├── database.py       # Async SQLAlchemy engine
│   │   ├── redis.py          # Redis connection manager
│   │   ├── qdrant.py         # Qdrant vector DB client
│   │   ├── security.py       # JWT, bcrypt, Google OAuth
│   │   ├── geo.py            # PostGIS spatial helpers
│   │   ├── storage.py        # File storage (local/cloud)
│   │   ├── exceptions.py     # Custom HTTP exceptions
│   │   └── middleware.py     # Request logging middleware
│   ├── models/               # SQLAlchemy ORM models
│   ├── schemas/              # Pydantic request/response schemas
│   ├── workers/              # ARQ background workers
│   │   ├── worker.py         # Worker settings & task registration
│   │   ├── scheduler.py      # Periodic task scheduling
│   │   └── tasks/            # Background task implementations
│   └── scripts/
│       └── seed.py           # Dev database seeding
├── alembic/                  # Database migrations
├── Dockerfile                # Multi-stage Docker build
├── docker-compose.yml        # Full local stack
├── Makefile                  # Developer shortcuts
└── pyproject.toml            # Dependencies & tooling config
```

### Technology Stack

| Layer | Technology |
|---|---|
| **API Framework** | FastAPI 0.115+ (async) |
| **Language** | Python 3.12 |
| **ORM** | SQLAlchemy 2.0 (async) |
| **Database** | PostgreSQL 16 + PostGIS 3.4 |
| **Caching / Queue** | Redis 7 |
| **Background Jobs** | ARQ (async Redis queue) |
| **Vector DB** | Qdrant (semantic search) |
| **Embeddings** | sentence-transformers |
| **LLMs** | Google Gemini + Groq |
| **Auth** | JWT (python-jose) + Google OAuth2 |
| **Passwords** | bcrypt |
| **Geo** | GeoAlchemy2 + PostGIS |
| **Social Ingestion** | Twikit (Twitter) + AsyncPRAW (Reddit) |
| **Traffic** | TomTom Traffic API |
| **Migrations** | Alembic |
| **Linting/Format** | Ruff |
| **Containerization** | Docker + Docker Compose |
| **Package Manager** | uv |

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- (Optional) Python 3.12+ with `uv` for local dev

### 1. Clone & Configure

```bash
git clone https://github.com/ayyushutup/Chai-Sutta.git
cd Chai-Sutta
cp .env.example .env
```

Edit `.env` and fill in your API keys (see [Environment Variables](#-environment-variables)).

### 2. Start the Full Stack

```bash
make up
```

This spins up:
- `api` — FastAPI server on **http://localhost:8000**
- `postgres` — PostgreSQL 16 + PostGIS on port 5432
- `redis` — Redis 7 on port 6379
- `qdrant` — Qdrant vector DB on ports 6333/6334
- `worker` — ARQ background worker

### 3. Run Migrations & Seed

```bash
make migrate   # Run Alembic migrations
make seed      # Seed the database with sample data
```

### 4. Explore the API

| URL | Description |
|---|---|
| http://localhost:8000 | Health check |
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc |

---

## 💻 Local Development (without Docker)

```bash
# Install uv
pip install uv

# Create virtualenv and install dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Start external services (Postgres, Redis, Qdrant) via Docker
docker compose up postgres redis qdrant -d

# Run migrations
make migrate

# Start dev server with hot reload
make dev
```

### Useful Make Targets

| Command | Description |
|---|---|
| `make dev` | Run dev server with `--reload` |
| `make up` | Bring up full Docker stack |
| `make down` | Tear down stack (removes volumes) |
| `make migrate` | Apply all pending Alembic migrations |
| `make migrate-create` | Interactively create a new migration |
| `make seed` | Seed database with sample data |
| `make worker` | Start ARQ background worker |
| `make test` | Run pytest with coverage |
| `make lint` | Lint with Ruff |
| `make format` | Format + auto-fix with Ruff |
| `make clean` | Remove Python cache artifacts |

---

## 🌐 API Reference

Base path: `/api/v1`

### Authentication — `/auth`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | ❌ | Register with email & password |
| `POST` | `/auth/login` | ❌ | Login (OAuth2 password form) |
| `POST` | `/auth/google` | ❌ | Authenticate via Google ID token |
| `GET` | `/auth/me` | ✅ | Get current user profile |

### News — `/news`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/news/` | ❌ | List news (filter by city/zone/category) |
| `GET` | `/news/{id}` | ❌ | Get a single article |

### Weather — `/weather`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/weather/` | ❌ | Current weather for a city |

### Traffic — `/traffic`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/traffic/` | ❌ | Traffic incidents for a city |

### Trains — `/trains`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/trains/` | ❌ | Live train status list |

### Events — `/events`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/events/` | ❌ | List city events |
| `POST` | `/events/` | ✅ | Create an event |
| `GET` | `/events/{id}` | ❌ | Get a single event |

### Community Reports — `/reports`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/reports/` | ❌ | List reports (filter by city/zone/category) |
| `POST` | `/reports/` | ✅ | Create a report (with optional image) |
| `GET` | `/reports/nearby` | ❌ | Reports near lat/lon within radius |
| `GET` | `/reports/{id}` | ❌ | Get a single report |
| `POST` | `/reports/{id}/vote` | ✅ | Upvote or downvote a report |

### Search — `/search`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/search/` | ❌ | Semantic search across city content |

### City Intelligence — `/city-summary`, `/city-mood`, `/trending`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/city-summary/` | ❌ | AI-generated daily city summary |
| `GET` | `/city-mood/` | ❌ | City mood/sentiment score |
| `GET` | `/trending/` | ❌ | Trending topics in city |

### Ask Tapri — `/chat`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/chat/` | Optional | Chat with Tapri AI about the city |
| `GET` | `/chat/history` | ✅ | Get user's chat history |

### Profile — `/profile`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/profile/` | ✅ | Get user profile details |
| `PATCH` | `/profile/` | ✅ | Update user profile |

> **Swagger UI** at `/docs` provides full request/response schemas with try-it-out support.

---

## 🔐 Authentication

The API uses **JWT Bearer tokens** with a 24-hour expiry.

```
Authorization: Bearer <access_token>
```

Two sign-in methods are supported:

1. **Email/Password** — POST `/api/v1/auth/login` with `username` and `password` form fields
2. **Google OAuth** — POST `/api/v1/auth/google` with a Google ID token

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` and configure:

```ini
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/chaisutta

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=change-this-to-a-random-secret-in-production
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440   # 24 hours

# Google OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# LLM Providers
GEMINI_API_KEY=      # Google AI Studio (free tier available)
GROQ_API_KEY=        # Groq cloud (free tier available)

# Twitter/X (for social ingestion)
TWITTER_USERNAME=
TWITTER_EMAIL=
TWITTER_PASSWORD=

# Reddit API
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=chai-sutta:v1.0

# TomTom (traffic API — 2500 req/day free)
TOMTOM_API_KEY=

# Storage
STORAGE_BACKEND=local
LOCAL_STORAGE_PATH=./uploads

# Qdrant Vector DB
QDRANT_HOST=localhost
QDRANT_PORT=6333

# App
APP_ENV=development
APP_DEBUG=true
APP_HOST=0.0.0.0
APP_PORT=8000
```

---

## 🗄️ Data Models

| Model | Description |
|---|---|
| `City` | Top-level city entity |
| `Zone` | Neighbourhood/zone within a city |
| `User` | App user (email or Google auth) |
| `NewsArticle` | Hyperlocal news article |
| `WeatherData` | Weather snapshot for a city |
| `TrafficData` | Traffic incident or congestion event |
| `TrainStatus` | Live train running status |
| `Event` | City event or gathering |
| `CommunityReport` | User-submitted geo-tagged incident |
| `CitySummary` | AI-generated daily city digest |
| `SocialMention` | Social media mention (Twitter/Reddit) |
| `UserInteraction` | User engagement tracking |

All models include `created_at` / `updated_at` timestamps via `TimestampMixin`.

---

## ⚡ Background Workers

ARQ-powered workers handle heavy async tasks:

| Task Module | Responsibility |
|---|---|
| `ingestion_tasks` | Ingest news RSS feeds, social mentions, weather & traffic data |
| `ai_tasks` | Generate LLM city summaries, mood scores, and embed content for search |
| `summary_tasks` | Assemble and persist daily city digests |

Run the worker:

```bash
make worker
# or
arq app.workers.worker.WorkerSettings
```

---

## 🧪 Testing

```bash
make test
# or
pytest -v --cov=app --cov-report=term-missing
```

Tests live in `app/tests/` and use `pytest-asyncio` for async test support.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Follow the code style — run `make format` and `make lint` before committing
4. Commit with [Conventional Commits](https://www.conventionalcommits.org/) style
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

<div align="center">
  Built with ❤️ and ☕ — <em>chai pe charcha, sutta pe solutions</em>
</div>
