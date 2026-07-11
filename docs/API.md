# API Reference

Complete reference for all Chai Sutta REST API endpoints.

**Base URL**: `http://localhost:8000/api/v1`  
**Interactive docs**: `http://localhost:8000/docs` (Swagger UI)  
**OpenAPI spec**: `http://localhost:8000/redoc` (ReDoc)

---

## Authentication

Protected endpoints require a JWT Bearer token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Tokens are obtained from `/auth/register`, `/auth/login`, or `/auth/google`.  
Default expiry: **24 hours**.

---

## Health Check

### `GET /`

Returns service health status.

**Response `200`**
```json
{
  "status": "healthy",
  "service": "Chai Sutta API",
  "version": "0.1.0",
  "environment": "development"
}
```

---

## Authentication — `/api/v1/auth`

### `POST /auth/register`

Register a new user with email and password.

**Request Body**
```json
{
  "email": "user@example.com",
  "password": "strongpassword",
  "display_name": "Rahul"
}
```

**Response `201`**
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "display_name": "Rahul",
    "avatar_url": null,
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

**Errors**: `400` if email already registered.

---

### `POST /auth/login`

Authenticate with email and password (OAuth2 password form).

**Request** (form-encoded)
```
username=user@example.com&password=strongpassword
```

**Response `200`** — same as `/auth/register`.

**Errors**: `400` for incorrect credentials or deactivated account.

---

### `POST /auth/google`

Authenticate or register via a Google ID token.

**Request Body**
```json
{
  "token": "<google-id-token>"
}
```

**Response `200`** — same as `/auth/register`.

**Errors**: `401` for invalid or expired Google token.

---

### `GET /auth/me` 🔒

Get the currently authenticated user's profile.

**Response `200`**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "display_name": "Rahul",
  "avatar_url": null,
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

## News — `/api/v1/news`

### `GET /news/`

List news articles with optional filters.

**Query Parameters**

| Param | Type | Default | Description |
|---|---|---|---|
| `city_id` | UUID | — | Filter by city |
| `zone_id` | UUID | — | Filter by zone |
| `category` | string | — | News category |
| `page` | int | 1 | Page number |
| `page_size` | int | 20 | Items per page (max 100) |

**Response `200`** — Paginated list of news articles.
```json
{
  "items": [
    {
      "id": "uuid",
      "city_id": "uuid",
      "title": "Article Title",
      "summary": "Brief summary...",
      "source_url": "https://...",
      "image_url": null,
      "category": "local",
      "published_at": "2024-01-01T12:00:00Z",
      "created_at": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 20
}
```

---

### `GET /news/{id}`

Get a single news article by ID.

**Path Parameters**: `id` (UUID)

**Response `200`** — Single article object.  
**Errors**: `404` if not found.

---

## Weather — `/api/v1/weather`

### `GET /weather/`

Get current weather data for a city.

**Query Parameters**

| Param | Type | Required | Description |
|---|---|---|---|
| `city_id` | UUID | ✅ | City to get weather for |

**Response `200`**
```json
{
  "id": "uuid",
  "city_id": "uuid",
  "temperature": 28.5,
  "feels_like": 31.0,
  "humidity": 75,
  "description": "Partly cloudy",
  "wind_speed": 12.0,
  "recorded_at": "2024-01-01T12:00:00Z"
}
```

---

## Traffic — `/api/v1/traffic`

### `GET /traffic/`

Get traffic incidents for a city.

**Query Parameters**

| Param | Type | Required | Description |
|---|---|---|---|
| `city_id` | UUID | ✅ | City to query |

**Response `200`** — List of traffic incidents.

---

## Trains — `/api/v1/trains`

### `GET /trains/`

List live train statuses.

**Query Parameters**

| Param | Type | Default | Description |
|---|---|---|---|
| `city_id` | UUID | — | Filter by city |
| `train_number` | string | — | Specific train number |

**Response `200`** — List of train status objects.

---

## Events — `/api/v1/events`

### `GET /events/`

List city events.

**Query Parameters**

| Param | Type | Default | Description |
|---|---|---|---|
| `city_id` | UUID | — | Filter by city |
| `zone_id` | UUID | — | Filter by zone |
| `from_date` | date | — | Events on/after this date |
| `to_date` | date | — | Events on/before this date |
| `page` | int | 1 | Page number |
| `page_size` | int | 20 | Items per page |

---

### `POST /events/` 🔒

Create a new city event.

**Request Body**
```json
{
  "city_id": "uuid",
  "zone_id": "uuid",
  "title": "Street Festival",
  "description": "Annual street festival...",
  "start_time": "2024-02-01T18:00:00Z",
  "end_time": "2024-02-01T22:00:00Z",
  "lat": 28.6139,
  "lon": 77.2090
}
```

---

### `GET /events/{id}`

Get a single event by ID.

---

## Community Reports — `/api/v1/reports`

### `GET /reports/`

List community reports with optional filters.

**Query Parameters**

| Param | Type | Default | Description |
|---|---|---|---|
| `city_id` | UUID | — | Filter by city |
| `zone_id` | UUID | — | Filter by zone |
| `category` | string | — | e.g. `pothole`, `flooding`, `power_outage` |
| `status` | string | — | `unverified`, `verified`, `resolved` |
| `page` | int | 1 | Page number |
| `page_size` | int | 20 | Items per page |

**Response `200`**
```json
{
  "items": [
    {
      "id": "uuid",
      "user_id": "uuid",
      "city_id": "uuid",
      "zone_id": "uuid",
      "category": "pothole",
      "content": "Large pothole on MG Road near metro exit",
      "media_url": "/uploads/abc.jpg",
      "media_type": "image",
      "upvotes": 12,
      "downvotes": 1,
      "verification_status": "unverified",
      "created_at": "2024-01-01T09:00:00Z"
    }
  ],
  "total": 50,
  "page": 1,
  "page_size": 20
}
```

---

### `POST /reports/` 🔒

Create a community report with optional image upload.

**Request** (multipart/form-data)

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | ✅ | Short title |
| `description` | string | ✅ | Detailed description |
| `category` | string | ✅ | Report category |
| `city_id` | UUID | ✅ | City |
| `zone_id` | UUID | — | Zone (optional) |
| `lat` | float | — | Latitude |
| `lon` | float | — | Longitude |
| `image` | file | — | Image attachment (optional) |

**Response `201`** — Created report object.

---

### `GET /reports/nearby`

Get reports near a geographic point.

**Query Parameters**

| Param | Type | Default | Description |
|---|---|---|---|
| `lat` | float | ✅ | Latitude |
| `lon` | float | ✅ | Longitude |
| `radius_km` | float | 5.0 | Search radius (max 50 km) |

**Response `200`** — List of reports sorted by proximity.

---

### `GET /reports/{id}`

Get a single report by ID.

---

### `POST /reports/{id}/vote` 🔒

Upvote or downvote a report.

**Request Body**
```json
{ "vote_type": "up" }
```

`vote_type`: `"up"` | `"down"`

**Response `204 No Content`**

---

## Search — `/api/v1/search`

### `GET /search/`

Semantic search across all city content using vector similarity.

**Query Parameters**

| Param | Type | Default | Description |
|---|---|---|---|
| `q` | string | ✅ | Search query |
| `city_id` | UUID | — | Restrict to city |
| `limit` | int | 10 | Max results |

**Response `200`**
```json
{
  "results": [
    {
      "id": "uuid",
      "type": "news",
      "title": "...",
      "snippet": "...",
      "score": 0.92,
      "url": "/api/v1/news/uuid"
    }
  ]
}
```

---

## City Intelligence

### `GET /city-summary/`

Get the latest AI-generated daily city summary.

**Query Parameters**: `city_id` (UUID, required)

**Response `200`**
```json
{
  "id": "uuid",
  "city_id": "uuid",
  "summary": "Today in Bengaluru...",
  "highlights": ["Traffic on ORR", "Rain expected in evening"],
  "generated_at": "2024-01-01T06:00:00Z"
}
```

---

### `GET /city-mood/`

Get the current mood/sentiment score for a city.

**Query Parameters**: `city_id` (UUID, required)

**Response `200`**
```json
{
  "city_id": "uuid",
  "mood_score": 62.5,
  "mood_label": "Neutral",
  "breakdown": {
    "news": 0.6,
    "social": 0.65,
    "reports": 0.55
  },
  "computed_at": "2024-01-01T10:00:00Z"
}
```

---

### `GET /trending/`

Get trending topics in a city.

**Query Parameters**: `city_id` (UUID, required), `limit` (int, default 10)

**Response `200`** — List of trending topic strings/objects.

---

## Ask Tapri — `/api/v1/chat`

### `POST /chat/` (Auth optional)

Ask the Tapri AI assistant a question about the city.

**Request Body**
```json
{
  "message": "What's the traffic like near Connaught Place right now?",
  "city_id": "uuid",
  "context": {}
}
```

**Response `200`**
```json
{
  "id": "uuid",
  "message": "There are 3 active incidents near Connaught Place...",
  "sources": [
    { "type": "traffic", "id": "uuid" }
  ],
  "suggestions": [
    "Check Janpath area traffic",
    "What's the weather like?"
  ],
  "created_at": "2024-01-01T12:00:00Z"
}
```

> ⚠️ Anonymous users receive limited responses. Authenticate for full context.

---

### `GET /chat/history` 🔒

Get the authenticated user's chat history.

**Query Parameters**: `page`, `page_size`

---

## Profile — `/api/v1/profile`

### `GET /profile/` 🔒

Get the authenticated user's full profile.

---

### `PATCH /profile/` 🔒

Update user profile fields.

**Request Body** (partial update)
```json
{
  "display_name": "New Name",
  "avatar_url": "https://..."
}
```

---

## Common Response Formats

### Paginated Response

```json
{
  "items": [...],
  "total": 150,
  "page": 2,
  "page_size": 20
}
```

### Error Response

```json
{
  "detail": "Human-readable error message"
}
```

### HTTP Status Codes

| Code | Meaning |
|---|---|
| `200` | OK |
| `201` | Created |
| `204` | No Content |
| `400` | Bad Request |
| `401` | Unauthorized |
| `403` | Forbidden |
| `404` | Not Found |
| `409` | Conflict |
| `422` | Validation Error (Pydantic) |
| `500` | Internal Server Error |
