# Architecture Guide

This document describes the internal architecture of Chai Sutta, detailing how every layer fits together.

---

## System Diagram

```
                     ┌──────────────────────────────────────────────┐
                     │              Client / Mobile App              │
                     └──────────────────┬───────────────────────────┘
                                        │ HTTPS
                     ┌──────────────────▼───────────────────────────┐
                     │           FastAPI Application                 │
                     │  ┌────────────────────────────────────────┐  │
                     │  │  CORS · RequestLogging Middleware       │  │
                     │  └────────────────────────────────────────┘  │
                     │  ┌────────────────────────────────────────┐  │
                     │  │        REST API  /api/v1               │  │
                     │  │  auth · news · weather · traffic       │  │
                     │  │  trains · events · reports · search    │  │
                     │  │  city-summary · city-mood · chat       │  │
                     │  └──────────────┬─────────────────────────┘  │
                     └─────────────────┼────────────────────────────┘
              ┌──────────────┬─────────┴──────┬────────────────────┐
              │              │                │                    │
   ┌──────────▼──────┐  ┌───▼───┐  ┌─────────▼──────┐  ┌─────────▼──────┐
   │  PostgreSQL 16  │  │ Redis │  │   Qdrant DB    │  │ External APIs  │
   │  + PostGIS 3.4  │  │   7   │  │ (vector search)│  │ TomTom·Gemini  │
   │  (primary store)│  │(cache │  │                │  │ Groq·Reddit    │
   └─────────────────┘  │+queue)│  └────────────────┘  │ Twitter RSS    │
                        └───┬───┘                       └────────────────┘
                            │
                   ┌────────▼────────┐
                   │  ARQ Workers    │
                   │ ingestion tasks │
                   │  AI/LLM tasks  │
                   │ summary tasks   │
                   └─────────────────┘
```

---

## Application Startup

The entry point is `app/main.py` → `create_app()`.

On startup (`lifespan`), the following are initialized in order:
1. **PostgreSQL** async engine via `init_db()` (SQLAlchemy async)
2. **Redis** connection pool via `redis_manager.connect()`
3. **Qdrant** vector client via `qdrant_manager.init()`

On shutdown they are closed in reverse order.

---

## Request Lifecycle

```
Request
  │
  ▼
RequestLoggingMiddleware      ← logs method, path, status, latency
  │
  ▼
CORSMiddleware                ← allow-all in debug, restricted in prod
  │
  ▼
FastAPI Router (api/v1/)
  │
  ├─ Dependency injection
  │   ├─ get_db()             ← yields AsyncSession per request
  │   ├─ get_current_user()   ← validates JWT, fetches User row
  │   └─ get_current_user_optional()  ← same but returns None if unauth'd
  │
  ▼
Endpoint handler
  │
  ├─ ORM queries (SQLAlchemy async)
  ├─ Business logic
  └─ Returns Pydantic response model
```

---

## Authentication Flow

### Email / Password

```
POST /api/v1/auth/register
  → hash_password (bcrypt)
  → INSERT User (auth_provider="email")
  → create_access_token (JWT, HS256)

POST /api/v1/auth/login (OAuth2PasswordRequestForm)
  → SELECT User WHERE email = username
  → verify_password (bcrypt.checkpw)
  → create_access_token
```

### Google OAuth

```
POST /api/v1/auth/google  { token: "<google-id-token>" }
  → verify_google_token()
      → GET https://oauth2.googleapis.com/tokeninfo?id_token=...
      → validate aud == GOOGLE_CLIENT_ID
  → UPSERT User (auth_provider="google")
  → create_access_token
```

### Protected Endpoints

```python
# Bearer token extracted by OAuth2PasswordBearer
# Validated in get_current_user():
jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
→ payload["sub"]  # UUID string of user
→ SELECT User WHERE id = UUID(sub)
→ check user.is_active
```

---

## Database Layer

**Engine**: Async SQLAlchemy with `asyncpg` driver  
**Connection pool**: 20 connections, 10 overflow (configurable via env)  
**Extension**: PostGIS for geographic types and spatial queries

### Session Management

```python
# app/core/database.py
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
```

### Model Hierarchy

```
Base (DeclarativeBase)
  └── TimestampMixin (created_at, updated_at)
        ├── City
        │     └── Zone
        ├── User
        ├── NewsArticle
        ├── WeatherData
        ├── TrafficData
        ├── TrainStatus
        ├── Event
        ├── CommunityReport   ← has PostGIS `location` (POINT)
        ├── CitySummary
        ├── SocialMention
        └── UserInteraction
```

---

## Geographic / Spatial Queries

PostGIS functions are used via SQLAlchemy + GeoAlchemy2:

```python
# Find reports within 5 km
func.ST_DWithin(
    func.cast(CommunityReport.location, Geography),
    func.cast(point, Geography),
    5000,  # metres
)

# Sort by distance
func.ST_Distance(
    func.cast(CommunityReport.location, Geography),
    func.cast(func.ST_MakePoint(lon, lat), Geography),
)
```

Helpers in `app/core/geo.py`:
- `point_from_coords(lat, lon)` → WKT `POINT(lon lat)` string
- `nearby_filter(model, lat, lon, radius_km)` → SQLAlchemy filter clause

---

## Vector Search (Qdrant)

`QdrantManager` (`app/core/qdrant.py`) wraps the Qdrant Python client:

| Method | Description |
|---|---|
| `ensure_collection(name, vector_size)` | Create collection if it doesn't exist |
| `upsert_points(collection, points)` | Index embeddings |
| `search(collection, query_vector, filters, limit)` | ANN similarity search |
| `delete_points(collection, ids)` | Remove stale points |

Content is embedded using `sentence-transformers` models and stored per entity type (news, reports, events, etc.).

---

## Background Workers (ARQ)

ARQ uses Redis as the task queue. Tasks are defined in `app/workers/tasks/`:

| Module | Tasks |
|---|---|
| `ingestion_tasks.py` | Fetch news RSS, ingest weather/traffic, scrape social mentions |
| `ai_tasks.py` | Generate embeddings, produce LLM city summaries and mood scores |
| `summary_tasks.py` | Aggregate daily snapshots into `CitySummary` rows |

**WorkerSettings** (`app/workers/worker.py`):
- `max_jobs = 10` — max concurrent jobs
- `job_timeout = 600` — 10-minute timeout

**Scheduler** (`app/workers/scheduler.py`) defines cron-like periodic triggers for ingestion.

---

## LLM Integration

Two providers are supported, configured via environment variables:

| Provider | Env Key | Use |
|---|---|---|
| Google Gemini | `GEMINI_API_KEY` | City summaries, Ask Tapri chat |
| Groq | `GROQ_API_KEY` | Fast inference fallback |

The `chat.py` endpoint (`/api/v1/chat`) exposes **Ask Tapri**, a conversational assistant that answers questions about a city using live data from the database as context.

---

## File Storage

`app/core/storage.py` abstracts file uploads behind a `StorageBackend` interface:

| Backend | Config |
|---|---|
| `local` | Files saved to `LOCAL_STORAGE_PATH` (default: `./uploads`) |
| Cloud (future) | S3-compatible or GCS |

Community report images are stored via this abstraction and served at `/uploads/<filename>`.

---

## Error Handling

Custom exceptions in `app/core/exceptions.py` map to HTTP status codes:

| Exception | Status |
|---|---|
| `BadRequestException` | 400 |
| `UnauthorizedException` | 401 |
| `ForbiddenException` | 403 |
| `NotFoundException` | 404 |
| `ConflictException` | 409 |

All handlers are registered on the FastAPI app via `register_exception_handlers(app)` and return a consistent `{ "detail": "..." }` JSON body.

---

## Configuration

All settings are declared in `app/config.py` using **pydantic-settings**, loaded from `.env` (case-insensitive, extra values ignored). A single `settings` singleton is imported throughout the codebase.
