# Epidemic Sound API - Complete Technical Reference

**Last Updated:** December 2025
**Base API URL:** `https://partner-content-api.epidemicsound.com/v0/`
**Documentation Portal:** https://developers.epidemicsite.com/docs/

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Search & Discovery Endpoints](#search--discovery-endpoints)
4. [Track Metadata](#track-metadata)
5. [Download Endpoints](#download-endpoints)
6. [Streaming & Playback](#streaming--playback)
7. [Advanced Features](#advanced-features)
8. [Rate Limits & Quotas](#rate-limits--quotas)
9. [Error Handling](#error-handling)
10. [Pagination](#pagination)
11. [Licensing & Usage](#licensing--usage)
12. [SDKs & Code Examples](#sdks--code-examples)

---

## Overview

### Core Requirements

**Content Format:** All requests and responses use `application/json`

**Versioning:** Path-prefixed versioning (`/v0/`, `/v1/`, etc.) maintains backward compatibility. Existing endpoints and fields remain stable within a version.

**CORS:** Production environments enforce Cross-Origin Resource Sharing restrictions. Web applications may require domain whitelisting through the developer portal under "Authentication settings" > "Web Origins."

**DDoS Protection:** The API uses web application firewall protections that may occasionally respond with `502 Bad Gateway` errors during attack mitigation. Implement exponential backoff for retries.

### Access Levels

- **Free Tier:** Access to curated selection of free tracks
- **Full Library:** 40,000+ tracks with personalized content (requires OAuth)

---

## Authentication

### Two Authentication Flows

#### 1. Partner Authentication Flow (Free Tracks Access)

This two-step process provides access to curated free tracks:

**Step 1: Obtain Partner Token**

```bash
POST https://partner-content-api.epidemicsound.com/v0/partner-token
Content-Type: application/json

{
  "accessKeyId": "{YOUR_ACCESS_KEY_ID}",
  "accessKeySecret": "{YOUR_ACCESS_KEY_SECRET}"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": 86400
}
```

**Token Details:**
- **TTL:** 1 day (24 hours)
- **Purpose:** Enables subsequent user token requests
- **Best Practice:** Cache partner tokens in backend rather than sending credentials from client apps

**Step 2: Generate User Token**

```bash
POST https://partner-content-api.epidemicsound.com/v0/token
Authorization: Bearer {PARTNER_TOKEN}
Content-Type: application/json

{
  "userId": "unique-anonymized-identifier"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": 604800
}
```

**Token Details:**
- **TTL:** 7 days
- **User ID Requirements:** Use anonymized, one-way hashed versions of internal user identifiers (GDPR-compliant)
- **Token Independence:** User tokens remain valid even if partner token expires

#### 2. OAuth 2.0 / OpenID Connect Flow (Full Library Access)

Uses "Authorization Code Flow with Proof Key for Code Exchange (PKCE)".

**Authorization Endpoint:**
```
https://login.epidemicsound.com/auth/realms/accounts/protocol/openid-connect/auth
```

**Token Exchange Endpoint:**
```
https://login.epidemicsound.com/auth/realms/accounts/protocol/openid-connect/token
```

**Step 1: Authorization Request**

```
GET https://login.epidemicsound.com/auth/realms/accounts/protocol/openid-connect/auth
  ?response_type=code
  &client_id={YOUR_CLIENT_ID}
  &redirect_uri={YOUR_REGISTERED_CALLBACK_URL}
  &code_challenge={SHA256_BASE64_ENCODED_VERIFIER}
  &code_challenge_method=S256
  &state={OPTIONAL_CSRF_TOKEN}
```

**Parameters:**
- `response_type`: "code"
- `client_id`: Your application's ID
- `redirect_uri`: Pre-registered callback URL
- `code_challenge`: SHA256-hashed, Base64-encoded `code_verifier`
- `code_challenge_method`: "S256"
- `state` (optional): CSRF prevention token

**User Flow:**
1. User authenticates and authorizes application
2. Redirect to callback URL with authorization code
3. Authorization code expires in 10 minutes

**Step 2: Token Exchange**

```bash
POST https://login.epidemicsound.com/auth/realms/accounts/protocol/openid-connect/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code={AUTHORIZATION_CODE}
&code_verifier={ORIGINAL_UNHASHED_VERIFIER}
&redirect_uri={YOUR_CALLBACK_URL}
&client_id={YOUR_CLIENT_ID}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "token_type": "Bearer"
}
```

**Token Lifetimes:**
- `access_token`: 300 seconds (5 minutes)
- `refresh_token`: 1800 seconds (30 minutes)

**Step 3: Token Refresh**

```bash
POST https://login.epidemicsound.com/auth/realms/accounts/protocol/openid-connect/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&refresh_token={REFRESH_TOKEN}
&client_id={YOUR_CLIENT_ID}
```

**Step 4: Logout**

```bash
POST https://login.epidemicsound.com/auth/realms/accounts/protocol/openid-connect/logout
Content-Type: application/x-www-form-urlencoded

client_id={YOUR_CLIENT_ID}
&refresh_token={CURRENT_REFRESH_TOKEN}
```

Returns HTTP 204 No Content on success.

### Security Recommendations

- Use system browser components (Custom Tabs on Android, ASWebAuthenticationSession on iOS 13+)
- Never use embedded web views for OAuth flows
- Utilize official SDKs for handling OAuth complexity

---

## Search & Discovery Endpoints

### 1. Search Tracks

**Endpoint:** `GET /v0/tracks/search`

**Description:** Search the entire Epidemic Sound library with semantic search capabilities using open language models (e.g., "music for a calm beach scene").

**Query Parameters:**

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `term` | string | Yes | Search query text | - |
| `offset` | int32 | No | Starting position in results | 0 |
| `limit` | int32 | No | Results per page | 50 (max: 60) |
| `genre` | string[] | No | Filter by genre IDs | - |
| `mood` | string[] | No | Filter by mood IDs | - |
| `sort` | string | No | Sort by: Relevance, Date, Title | Relevance |
| `order` | string | No | Order: asc, desc | asc |

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/tracks/search?term=happy+upbeat&genre=electronic&mood=energetic&limit=25
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

**Response Structure:**

```json
{
  "tracks": [
    {
      "id": "6rUPerw2po",
      "mainArtists": ["Main Artist"],
      "featuredArtists": ["Featured Artist"],
      "title": "Happy Song",
      "bpm": 135,
      "length": 3123,
      "moods": [
        {"id": "happy", "name": "Happy"},
        {"id": "eccentric", "name": "Eccentric"}
      ],
      "genres": [
        {
          "id": "beats",
          "name": "Beats",
          "parent": {"id": "parent", "name": "Parent Beats"}
        }
      ],
      "images": {
        "default": "https://cdn.epidemicsound.com/...",
        "XS": "https://cdn.epidemicsound.com/...",
        "S": "https://cdn.epidemicsound.com/...",
        "M": "https://cdn.epidemicsound.com/...",
        "L": "https://cdn.epidemicsound.com/..."
      },
      "waveformUrl": "https://pdn.epidemicsound.com/waveforms/1600/394079.json",
      "hasVocals": true,
      "added": "2020-10-10",
      "tierOption": "FREE",
      "isExplicit": false,
      "isPreviewOnly": true
    }
  ],
  "pagination": {
    "page": 2,
    "limit": 25,
    "offset": 25
  },
  "links": {
    "next": "/tracks/search?limit=25&offset=50",
    "prev": "/tracks/search?limit=25&offset=0"
  },
  "aggregations": {
    "moods": [
      {"id": "energetic", "name": "Energetic", "count": 1}
    ],
    "genres": [
      {"id": "rock", "name": "Rock", "count": 1}
    ]
  }
}
```

### 2. List Tracks by Filters

**Endpoint:** `GET /v0/tracks`

**Description:** List all tracks based on mood, genre, or BPM filters.

**Query Parameters:**

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `genre` | string[] | No | One or more genre identifiers | - |
| `mood` | string[] | No | One or more mood identifiers | - |
| `bpmMin` | int32 | No | Minimum BPM threshold | - |
| `bpmMax` | int32 | No | Maximum BPM threshold | - |
| `limit` | int32 | No | Results per page | 50 (max: 100) |
| `offset` | int32 | No | Starting position | 0 |

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/tracks?mood=happy&bpmMin=120&bpmMax=140&limit=50
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

**Response:** Same structure as search endpoint.

### 3. Collections (Curated Playlists)

**Endpoint:** `GET /v0/collections`

**Description:** Returns curated playlists organized by Epidemic Sound's expert team. Maximum 20 tracks per collection in response.

**Query Parameters:**

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `excludeField` | string | No | Set to "tracks" to omit track data | - |
| `limit` | int32 | No | Maximum entries returned | 10 (max: 20) |
| `offset` | int32 | No | Index position | 0 |

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/collections?limit=20
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

**Response Structure:**

```json
{
  "collections": [
    {
      "id": "uuid-format-id",
      "name": "Summer Vibes",
      "trackCount": 45,
      "availableTrackCount": 20,
      "images": {
        "default": "https://cdn.epidemicsound.com/...",
        "XS": "...",
        "S": "...",
        "M": "...",
        "L": "..."
      },
      "tracks": [
        {
          "id": "trackId",
          "title": "Track Title",
          "mainArtists": ["Artist Name"],
          "bpm": 125,
          "length": 180,
          "moods": [...],
          "genres": [...],
          "tierOption": "FREE"
        }
      ]
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "offset": 0
  },
  "links": {
    "next": "/collections?limit=20&offset=20",
    "prev": null
  }
}
```

**Get Specific Collection:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/collections/{collectionId}
Authorization: Bearer {USER_ACCESS_TOKEN}
```

### 4. Browse by Moods

**Endpoint:** `GET /v0/moods`

**Description:** Browse music catalog by moods (happy, epic, relaxing, etc.) with cover artwork.

**Query Parameters:**

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `type` | string | No | "all", "featured", or "partner-tier" | all |
| `sort` | string | No | "alphabetic" or "relevance" | relevance |
| `order` | string | No | "asc" or "desc" | desc |
| `limit` | int32 | No | Maximum entries | 20 |
| `offset` | int32 | No | Pagination index | 0 |

**Type Options:**
- `all`: Complete Epidemic Sound library
- `featured`: Only moods curated/featured on epidemicsound.com
- `partner-tier`: Content available within your subscription level

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/moods?type=featured&sort=alphabetic&order=asc
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

**Response Structure:**

```json
{
  "moods": [
    {
      "id": "happy",
      "name": "Happy",
      "images": {
        "default": "https://cdn.epidemicsound.com/...",
        "XS": "...",
        "S": "...",
        "M": "...",
        "L": "..."
      },
      "tracks": [...]
    }
  ],
  "pagination": {...},
  "links": {...},
  "aggregations": {...}
}
```

**Get Mood Details:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/moods/{moodId}
Authorization: Bearer {USER_ACCESS_TOKEN}
```

### 5. Browse by Genres

**Endpoint:** `GET /v0/genres`

**Description:** Browse by genres (rock, hip-hop, acoustic, etc.) with parent-child relationships.

**Query Parameters:** Similar to moods endpoint

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/genres?type=featured
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

**Get Genre Details:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/genres/{genreId}
Authorization: Bearer {USER_ACCESS_TOKEN}
```

### 6. Search Autosuggest

**Endpoint:** `GET /v0/tracks/suggestions`

**Description:** Get autocomplete suggestions for search queries.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `term` | string | Yes | Partial search query |

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/tracks/suggestions?term=hap
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

---

## Track Metadata

### Track Object Structure

All track objects contain the following fields:

```json
{
  "id": "string",
  "title": "string",
  "mainArtists": ["string"],
  "featuredArtists": ["string"],
  "bpm": 120,
  "length": 180,
  "moods": [
    {
      "id": "string",
      "name": "string"
    }
  ],
  "genres": [
    {
      "id": "string",
      "name": "string",
      "parent": {
        "id": "string",
        "name": "string"
      }
    }
  ],
  "images": {
    "default": "url",
    "XS": "url",
    "S": "url",
    "M": "url",
    "L": "url"
  },
  "waveformUrl": "url",
  "hasVocals": true,
  "added": "YYYY-MM-DD",
  "tierOption": "FREE | PAID",
  "isExplicit": false,
  "isPreviewOnly": true
}
```

### Field Descriptions

- **id:** Unique track identifier
- **title:** Track name
- **mainArtists:** Primary artists (array)
- **featuredArtists:** Featured artists (array)
- **bpm:** Beats per minute (tempo)
- **length:** Duration in seconds
- **moods:** Array of mood objects with id and name
- **genres:** Array of genre objects with parent genre info
- **images:** Cover art in multiple resolutions
- **waveformUrl:** URL to JSON waveform data (~1600 min/max value pairs)
- **hasVocals:** Boolean indicating vocal presence
- **added:** Release date (YYYY-MM-DD format)
- **tierOption:** FREE or PAID tier availability
- **isExplicit:** Boolean for explicit content flag
- **isPreviewOnly:** Boolean indicating preview-only status

### Get Track Parameters

**Endpoint:** `GET /v0/tracks/parameters`

**Description:** Get available query options for filtering tracks.

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/tracks/parameters
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

---

## Download Endpoints

### Download Track (MP3)

**Endpoint:** `GET /v0/tracks/{trackId}/download`

**Description:** Retrieve MP3 files in two quality tiers. WAV format is NOT available.

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `trackId` | string | Yes | Track identifier |

**Query Parameters:**

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `format` | string | Yes | File format (only "mp3" supported) | mp3 |
| `quality` | string | No | "normal" (128kbps) or "high" (320kbps) | normal |

**Quality Options:**
- **Normal (128kbps):** Suitable for most use cases, 24-hour expiration
- **High (320kbps):** Premium content requirements, 1-hour expiration

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/tracks/6rUPerw2po/download?format=mp3&quality=high
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

**Response:**

```json
{
  "url": "https://download.epidemicsound.com/signed-url...",
  "expires": "2025-12-22T15:30:00Z"
}
```

**Response Details:**
- `url`: Signed download URL
- `expires`: ISO 8601 timestamp for URL expiration

**Expiration Times:**
- Normal quality: 24 hours
- High quality: 1 hour (10 minutes in some docs)

**Access Requirements:**
- Free tier users: Can download tracks marked as "FREE"
- Premium library: Requires active subscription (403 status if unauthorized)

### Download Sound Effect

**Endpoint:** `GET /v0/sound-effects/{sfxId}/download`

**Description:** Download sound effects in MP3 format.

**Parameters:** Same as track download endpoint

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/sound-effects/{sfxId}/download?format=mp3&quality=high
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

---

## Streaming & Playback

### HLS Streaming (Recommended)

**Endpoint:** `GET /v0/tracks/{trackId}/stream`

**Description:** Stream tracks using HLS (HTTP Live Streaming) format for preview/playback. Recommended over MP3 due to smaller file transfers and adaptive quality.

**Benefits over MP3:**
- Smaller file transfers
- Adaptive quality streaming (switches to lower quality when necessary)
- AAC encoding (smaller footprint, similar quality to MP3)

**Audio Encoding:** AAC (Advanced Audio Coding) standard

**Quality Streams:** Primary manifest refers to two variant quality streams. HLS client libraries automatically choose optimal quality based on download speed.

**Access:** No subscription or account connection required for streaming (allows listening before account connection).

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/tracks/6rUPerw2po/stream
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

**Response:**

```json
{
  "url": "https://streaming.epidemicsound.com/hls/master.m3u8"
}
```

### Waveform Data

**Description:** All tracks include waveform data in JSON format.

**Access:** Via `waveformUrl` field in track metadata

**Waveform Specifications:**
- **Resolution:** 8-bit
- **Data Points:** ~1600 minimum and maximum value pairs
- **Format:** JSON with waveform data points and meta-information

**Example Waveform URL:**
```
https://pdn.epidemicsound.com/waveforms/1600/394079.json
```

**Use Cases:**
- Visual representation in audio players
- Segment selection interfaces
- Timeline visualization

### Beats (Timestamp Data)

**Endpoint:** `GET /v0/tracks/{trackId}/beats`

**Description:** Get beat timestamp data for synchronization (e.g., cutting video in sync with music).

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/tracks/6rUPerw2po/beats
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

**Response:**

```json
{
  "beats": [
    {"timestamp": 0.5},
    {"timestamp": 1.0},
    {"timestamp": 1.5}
  ]
}
```

---

## Advanced Features

### 1. Similar Tracks

**Endpoint:** `GET /v0/tracks/{trackId}/similar`

**Description:** Retrieve tracks with similar characteristics (genre, mood, tempo).

**Query Parameters:**

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `limit` | int32 | No | Results per page | 10 |
| `offset` | int32 | No | Starting position | 0 |

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/tracks/6rUPerw2po/similar?limit=20
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

### 2. Similar Track Segments (EAR Technology)

**Endpoint (by Track ID):** `GET /v0/tracks/{trackId}/similar-segments`

**Description:** Find alternative music segments using Epidemic Audio Reference (EAR) technology based on part of a track.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `timestamp` | float | Yes | Starting point in seconds |
| `duration` | float | No | Segment duration in seconds |

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/tracks/6rUPerw2po/similar-segments?timestamp=30.5&duration=10
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

**Endpoint (by Uploaded Audio):** `POST /v0/audio/upload/partner`

**Description:** Upload external audio file to find similar segments.

**File Requirements:**
- Supported formats specified in documentation
- Checksum endpoint prevents duplicate uploads

### 3. Soundmatch (Image-Based Recommendations)

AI-powered feature that analyzes video frames to recommend suitable tracks.

**Step 1: Upload Image**

**Endpoint:** `POST /v0/images/upload`

**Description:** Upload JPEG image from user's video.

**File Requirements:**
- Format: JPEG only
- Size limit: 2MB

**Example Request:**

```bash
POST https://partner-content-api.epidemicsound.com/v0/images/upload
Authorization: Bearer {USER_ACCESS_TOKEN}
Content-Type: multipart/form-data

[Binary image data]
```

**Response:**

```json
{
  "imageId": "unique-image-id"
}
```

**Step 2: Get Recommendations**

**Endpoint:** `GET /v0/images/{imageId}/recommendations`

**Example Request:**

```bash
GET https://partner-content-api.epidemicsound.com/v0/images/unique-image-id/recommendations
Authorization: Bearer {USER_ACCESS_TOKEN}
Accept: application/json
```

**Response:** Array of recommended tracks

**Privacy Requirements:**
- Privacy policy must inform users about image uploads
- Must provide users capability to delete uploaded content
- Implement user consent mechanism

### 4. Popular Segments (ML-Powered)

**Description:** ML-powered track segment recommendations based on YouTube streaming data.

**Use Case:** Discover the most popular parts of tracks based on actual usage patterns.

---

## Rate Limits & Quotas

### Rate Limiting Overview

All requests are subject to daily rate limits designed to prevent abuse without limiting legitimate usage.

### Rate Limit Details

- **Period:** Daily
- **Specific Quota:** Not publicly disclosed (allocated per application)
- **Custom Limits:** Contact Epidemic Sound for higher limits

### Monitoring Rate Limits

**Response Headers:**

```
X-RateLimit-Reset: 2025-12-23T00:00:00Z
X-RateLimit-Reached: false
```

**Header Descriptions:**
- `X-RateLimit-Reset`: Time in GMT until next reset of rate limiter
- `X-RateLimit-Reached`: Boolean indicating if limit exceeded

### Notifications

You will receive email notifications when approaching allocated rate limit.

### Best Practices

1. **Exponential Backoff:** Implement delays for request retries
2. **Cache Partner Tokens:** Cache tokens in backend (valid for 24 hours)
3. **Batch Operations:** Use bulk endpoints when available
4. **Monitor Headers:** Check rate limit headers in responses
5. **Request Limit Increases:** Contact support if legitimate usage requires higher limits

### DDoS Protection

API uses web application firewall protections. If you receive `502 Bad Gateway` errors:
- Implement exponential backoff delays for retries
- This helps distinguish legitimate clients from malicious traffic

---

## Error Handling

### HTTP Status Codes

| Status Code | Description | Action |
|-------------|-------------|--------|
| 200 | Success | Process response |
| 204 | No Content | Operation completed (e.g., logout) |
| 400 | Bad Request | Check request parameters and format |
| 401 | Unauthorized | Token expired or invalid, re-authenticate |
| 403 | Forbidden | Access denied (e.g., premium content without subscription) |
| 429 | Too Many Requests | Rate limit exceeded, implement backoff |
| 502 | Bad Gateway | DDoS protection active, retry with exponential backoff |
| 503 | Service Unavailable | Temporary service issue, retry later |

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_TOKEN",
    "message": "The provided access token has expired",
    "details": {
      "expiredAt": "2025-12-22T10:00:00Z"
    }
  }
}
```

### Common Error Scenarios

**1. Token Expiration (401)**

```json
{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Access token has expired"
  }
}
```

**Solution:** Request new user token (partner flow) or refresh access token (OAuth flow)

**2. Rate Limit Exceeded (429)**

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Daily request limit reached"
  }
}
```

**Solution:** Wait for rate limit reset (check `X-RateLimit-Reset` header) or request limit increase

**3. Access Denied (403)**

```json
{
  "error": {
    "code": "SUBSCRIPTION_REQUIRED",
    "message": "This track requires an active subscription"
  }
}
```

**Solution:** User needs active Epidemic Sound subscription or select free tier tracks

**4. Invalid Parameters (400)**

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Limit parameter must be between 1 and 60",
    "parameter": "limit"
  }
}
```

**Solution:** Validate request parameters against API specifications

### Retry Strategy

**Recommended Exponential Backoff:**

```python
import time

def make_api_request_with_retry(url, max_retries=5):
    for attempt in range(max_retries):
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 429:
            # Rate limit exceeded
            retry_after = int(response.headers.get('X-RateLimit-Reset', 60))
            time.sleep(retry_after)
            continue

        if response.status_code == 502:
            # DDoS protection, exponential backoff
            delay = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
            continue

        if response.status_code in [401, 403]:
            # Auth error, don't retry
            raise AuthenticationError(response.json())

        # Other errors
        response.raise_for_status()

    raise MaxRetriesExceeded()
```

---

## Pagination

### Pagination Pattern

All list endpoints use offset-based pagination.

### Pagination Parameters

| Parameter | Type | Description | Default |
|-----------|------|----------|---------|
| `limit` | int32 | Number of results per page | Varies by endpoint |
| `offset` | int32 | Starting position (0-indexed) | 0 |

### Pagination Limits by Endpoint

- **Search:** Default 50, max 60
- **Tracks:** Default 50, max 100
- **Collections:** Default 10, max 20
- **Moods/Genres:** Default/max 20

### Pagination Response Structure

```json
{
  "data": [...],
  "pagination": {
    "page": 2,
    "limit": 25,
    "offset": 25,
    "total": 1000
  },
  "links": {
    "next": "/tracks/search?limit=25&offset=50",
    "prev": "/tracks/search?limit=25&offset=0",
    "first": "/tracks/search?limit=25&offset=0",
    "last": "/tracks/search?limit=25&offset=975"
  }
}
```

### Pagination Navigation Example

```python
def fetch_all_tracks(search_term):
    all_tracks = []
    offset = 0
    limit = 60  # Max for search endpoint

    while True:
        response = requests.get(
            f"https://partner-content-api.epidemicsound.com/v0/tracks/search",
            params={
                "term": search_term,
                "limit": limit,
                "offset": offset
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )

        data = response.json()
        all_tracks.extend(data["tracks"])

        # Check if there's a next page
        if not data["links"].get("next"):
            break

        offset += limit

    return all_tracks
```

---

## Licensing & Usage

### License Tiers

**Free Tier:**
- Access to curated selection of free tracks
- Personal license for online posting
- No commercial use/monetization

**Paid Subscription (via ES Connect):**
- Full library access (40,000+ tracks)
- Commercial license
- Monetization and promotional use enabled

### Usage Reporting

**Endpoint:** `POST /v0/usage`

**Description:** Report track usage when users export to social media or download content.

**Required:** Report usage for attribution, analytics, and personalization improvements.

**Request Body:**

```json
{
  "trackId": "6rUPerw2po",
  "userId": "anonymized-user-id",
  "platform": "youtube",
  "timestamp": "2025-12-22T10:00:00Z"
}
```

**Supported Platforms:**
- youtube
- tiktok
- instagram
- facebook
- twitch
- twitter
- local (downloaded to device)
- other

**Bulk Reporting:**

**Endpoint:** `POST /v0/usage/bulk`

**Description:** Report multiple usage events in a single request.

**Request Body:**

```json
{
  "events": [
    {
      "trackId": "track1",
      "userId": "user1",
      "platform": "youtube",
      "timestamp": "2025-12-22T10:00:00Z"
    },
    {
      "trackId": "track2",
      "userId": "user1",
      "platform": "instagram",
      "timestamp": "2025-12-22T10:05:00Z"
    }
  ]
}
```

### Data Usage Policy

**Metadata Caching:**
- Prohibited by Acceptable Use Policy
- Always fetch fresh metadata from API

**User Data:**
- Use anonymized, one-way hashed user identifiers
- GDPR compliance required
- Provide data deletion capabilities for uploaded content (images, audio)

---

## SDKs & Code Examples

### Official SDKs

Epidemic Sound provides official SDKs through standard package managers:

**Available Languages:**
- JavaScript/TypeScript (npm)
- Python (PyPI)
- Java (Maven)

### TypeScript SDK

**Installation:**

```bash
npm install epidemic-sound-typescript-sdk
```

**Setup:**

```typescript
import { EpidemicSound } from 'epidemic-sound-typescript-sdk';

const epidemicSound = new EpidemicSound({
  partnerAuth: "YOUR_PARTNER_TOKEN",
  userAuth: "YOUR_USER_TOKEN",
  clientId: "YOUR_CLIENT_ID",
  clientSecret: "YOUR_CLIENT_SECRET",
  redirectUri: "YOUR_REDIRECT_URI"
});
```

**Authentication Methods:**

1. Partner Authentication
2. User Authentication
3. OpenID Connect (OAuth 2.0)

**Key Methods (37 total):**

```typescript
// Collections
await epidemicSound.collections();
await epidemicSound.collection(collectionId);

// Search
await epidemicSound.tracksSearchList({
  term: "happy upbeat",
  genre: ["electronic"],
  mood: ["energetic"],
  limit: 25
});

// Tracks
await epidemicSound.tracks.tracks({
  genre: ["rock"],
  bpmMin: 120,
  bpmMax: 140
});

// Parameters
await epidemicSound.tracks.listParameters();

// Suggestions
await epidemicSound.trackSuggestionsGet({
  term: "hap"
});
```

### Python Example (Conceptual)

```python
from epidemic_sound import EpidemicSoundClient

# Initialize client
client = EpidemicSoundClient(
    access_key_id="YOUR_ACCESS_KEY_ID",
    access_key_secret="YOUR_ACCESS_KEY_SECRET"
)

# Get partner token
partner_token = client.get_partner_token()

# Get user token
user_token = client.get_user_token(
    partner_token=partner_token,
    user_id="anonymized-user-id"
)

# Search tracks
results = client.search_tracks(
    user_token=user_token,
    term="energetic workout music",
    genre=["electronic", "rock"],
    bpm_min=120,
    bpm_max=140,
    limit=50
)

# Download track
download_url = client.get_download_url(
    user_token=user_token,
    track_id="6rUPerw2po",
    quality="high"
)

# Stream track
stream_url = client.get_stream_url(
    user_token=user_token,
    track_id="6rUPerw2po"
)
```

### cURL Examples

**Complete Workflow:**

```bash
# 1. Get Partner Token
curl -X POST https://partner-content-api.epidemicsound.com/v0/partner-token \
  -H "Content-Type: application/json" \
  -d '{
    "accessKeyId": "YOUR_ACCESS_KEY_ID",
    "accessKeySecret": "YOUR_ACCESS_KEY_SECRET"
  }'

# Response: {"token": "partner_token_here", "expiresIn": 86400}

# 2. Get User Token
curl -X POST https://partner-content-api.epidemicsound.com/v0/token \
  -H "Authorization: Bearer PARTNER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "anonymized-user-id"
  }'

# Response: {"token": "user_token_here", "expiresIn": 604800}

# 3. Search Tracks
curl -X GET "https://partner-content-api.epidemicsound.com/v0/tracks/search?term=happy&mood=energetic&limit=25" \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Accept: application/json"

# 4. Download Track
curl -X GET "https://partner-content-api.epidemicsound.com/v0/tracks/6rUPerw2po/download?format=mp3&quality=high" \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Accept: application/json"

# 5. Stream Track
curl -X GET "https://partner-content-api.epidemicsound.com/v0/tracks/6rUPerw2po/stream" \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Accept: application/json"

# 6. Report Usage
curl -X POST https://partner-content-api.epidemicsound.com/v0/usage \
  -H "Authorization: Bearer USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "trackId": "6rUPerw2po",
    "userId": "anonymized-user-id",
    "platform": "youtube",
    "timestamp": "2025-12-22T10:00:00Z"
  }'
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

class EpidemicSoundAPI {
  constructor(accessKeyId, accessKeySecret) {
    this.baseUrl = 'https://partner-content-api.epidemicsound.com/v0';
    this.accessKeyId = accessKeyId;
    this.accessKeySecret = accessKeySecret;
    this.partnerToken = null;
    this.userToken = null;
  }

  async getPartnerToken() {
    const response = await axios.post(`${this.baseUrl}/partner-token`, {
      accessKeyId: this.accessKeyId,
      accessKeySecret: this.accessKeySecret
    });

    this.partnerToken = response.data.token;
    return this.partnerToken;
  }

  async getUserToken(userId) {
    const response = await axios.post(
      `${this.baseUrl}/token`,
      { userId },
      {
        headers: {
          'Authorization': `Bearer ${this.partnerToken}`,
          'Content-Type': 'application/json'
        }
      }
    );

    this.userToken = response.data.token;
    return this.userToken;
  }

  async searchTracks(params) {
    const response = await axios.get(`${this.baseUrl}/tracks/search`, {
      params,
      headers: {
        'Authorization': `Bearer ${this.userToken}`,
        'Accept': 'application/json'
      }
    });

    return response.data;
  }

  async downloadTrack(trackId, quality = 'normal') {
    const response = await axios.get(
      `${this.baseUrl}/tracks/${trackId}/download`,
      {
        params: { format: 'mp3', quality },
        headers: {
          'Authorization': `Bearer ${this.userToken}`,
          'Accept': 'application/json'
        }
      }
    );

    return response.data;
  }

  async streamTrack(trackId) {
    const response = await axios.get(
      `${this.baseUrl}/tracks/${trackId}/stream`,
      {
        headers: {
          'Authorization': `Bearer ${this.userToken}`,
          'Accept': 'application/json'
        }
      }
    );

    return response.data;
  }

  async reportUsage(trackId, userId, platform) {
    const response = await axios.post(
      `${this.baseUrl}/usage`,
      {
        trackId,
        userId,
        platform,
        timestamp: new Date().toISOString()
      },
      {
        headers: {
          'Authorization': `Bearer ${this.userToken}`,
          'Content-Type': 'application/json'
        }
      }
    );

    return response.data;
  }
}

// Usage
(async () => {
  const api = new EpidemicSoundAPI(
    'YOUR_ACCESS_KEY_ID',
    'YOUR_ACCESS_KEY_SECRET'
  );

  // Authenticate
  await api.getPartnerToken();
  await api.getUserToken('anonymized-user-id');

  // Search tracks
  const searchResults = await api.searchTracks({
    term: 'upbeat energetic',
    mood: ['happy', 'energetic'],
    bpmMin: 120,
    bpmMax: 140,
    limit: 25
  });

  console.log('Found tracks:', searchResults.tracks.length);

  // Download first track
  if (searchResults.tracks.length > 0) {
    const trackId = searchResults.tracks[0].id;
    const downloadInfo = await api.downloadTrack(trackId, 'high');
    console.log('Download URL:', downloadInfo.url);
    console.log('Expires:', downloadInfo.expires);

    // Report usage
    await api.reportUsage(trackId, 'anonymized-user-id', 'youtube');
  }
})();
```

---

## Additional Resources

### Documentation Links

- **Main Documentation:** https://developers.epidemicsite.com/docs/
- **Getting Started:** https://developers.epidemicsite.com/docs/getting-started
- **Authentication Guide:** https://developers.epidemicsite.com/docs/auth
- **API Guides:** https://developers.epidemicsite.com/docs/guides
- **Swagger/OpenAPI Docs:** https://partner-content-api.epidemicsound.com/swagger
- **FAQ:** https://developers.epidemicsite.com/docs/FAQ

### Testing

**Production Credentials Testing:**
```
https://partner-content-api.epidemicsound.com/swagger
```

### GitHub Resources

- **Epidemic Sound GitHub:** https://github.com/epidemicsound
- **iOS Demo App:** https://github.com/epidemicsound/partner-content-api-demo-ios

### SDK Resources

- **TypeScript SDK (Konfig):** https://konfigthis.com/sdk/epidemic-sound/typescript/
- **All SDKs:** https://konfigthis.com/sdk/epidemic-sound/

### Support

For API support, rate limit increases, or technical questions:
- Contact through developer portal at developers.epidemicsound.com
- Email notifications for rate limit warnings

---

## Important Notes

### Adapt API Not Available

**Current Status:** The Adapt tool (AI-powered stem customization allowing individual control of melody, instruments, bass, and drums) is available through the web interface but **NOT accessible programmatically via the API** as of December 2025.

**Adapt Features (Web Only):**
- Select and adjust individual musical stems
- Mute or adjust volume of specific elements
- Mix and match stem-based adaptations
- Extend track length

**Alternative:** Contact Epidemic Sound for enterprise access to stem/Adapt API features.

### No WAV Format

MP3 is the only downloadable format. WAV is not currently supported via the API.

### No Stem Downloads

Individual stems (melody, instruments, bass, drums) cannot be downloaded separately via the API. This is a web-only feature through Adapt.

### Metadata Caching Prohibited

Do not cache track metadata. Always fetch fresh data from the API to ensure compliance with Acceptable Use Policy.

### GDPR Compliance Required

- Use anonymized, one-way hashed user identifiers
- Provide data deletion capabilities
- Obtain user consent for image uploads (Soundmatch)
- Implement privacy policy disclosures

---

## Quick Reference: Common Operations

### Search for Tracks

```bash
GET /v0/tracks/search?term={query}&mood={mood}&genre={genre}&limit=50
Authorization: Bearer {USER_TOKEN}
```

### Filter Tracks by BPM

```bash
GET /v0/tracks?bpmMin=120&bpmMax=140&limit=100
Authorization: Bearer {USER_TOKEN}
```

### Browse Collections

```bash
GET /v0/collections?limit=20
Authorization: Bearer {USER_TOKEN}
```

### Download Track

```bash
GET /v0/tracks/{trackId}/download?format=mp3&quality=high
Authorization: Bearer {USER_TOKEN}
```

### Stream Track

```bash
GET /v0/tracks/{trackId}/stream
Authorization: Bearer {USER_TOKEN}
```

### Get Similar Tracks

```bash
GET /v0/tracks/{trackId}/similar?limit=20
Authorization: Bearer {USER_TOKEN}
```

### Report Usage

```bash
POST /v0/usage
Authorization: Bearer {USER_TOKEN}
Content-Type: application/json

{
  "trackId": "{trackId}",
  "userId": "{anonymizedUserId}",
  "platform": "youtube"
}
```

---

**End of Epidemic Sound API Complete Technical Reference**

*For the most up-to-date information, always refer to the official documentation at https://developers.epidemicsite.com/docs/*
