"""
Epidemic Sound API Client - Production-Ready Python Implementation

A comprehensive, production-ready Python client for the Epidemic Sound Partner Content API.
Supports authentication, track search, download, streaming, and advanced features.

Documentation: https://developers.epidemicsite.com/docs/
API Base URL: https://partner-content-api.epidemicsound.com/v0/

Author: VideoGen YouTube Project
Last Updated: December 2025
"""

import os
import time
import json
import logging
import hashlib
import requests
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from functools import wraps
import random
from urllib.parse import urljoin, urlencode


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# EXCEPTIONS
# ============================================================================

class EpidemicSoundError(Exception):
    """Base exception for Epidemic Sound API errors."""
    pass


class AuthenticationError(EpidemicSoundError):
    """Raised when authentication fails."""
    pass


class RateLimitError(EpidemicSoundError):
    """Raised when rate limit is exceeded."""
    def __init__(self, message: str, reset_time: Optional[str] = None):
        super().__init__(message)
        self.reset_time = reset_time


class DownloadError(EpidemicSoundError):
    """Raised when download fails."""
    pass


class APIError(EpidemicSoundError):
    """Raised for general API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class TokenResponse:
    """Token response data."""
    token: str
    expires_in: int
    expires_at: Optional[datetime] = None

    def __post_init__(self):
        if self.expires_at is None:
            self.expires_at = datetime.utcnow() + timedelta(seconds=self.expires_in)

    def is_expired(self) -> bool:
        """Check if token is expired (with 5-minute buffer)."""
        return datetime.utcnow() >= (self.expires_at - timedelta(minutes=5))


@dataclass
class TrackMetadata:
    """Track metadata structure."""
    id: str
    title: str
    main_artists: List[str]
    featured_artists: List[str]
    bpm: int
    length: int  # Duration in seconds
    moods: List[Dict[str, str]]
    genres: List[Dict[str, Any]]
    images: Dict[str, str]
    waveform_url: str
    has_vocals: bool
    added: str  # Date in YYYY-MM-DD format
    tier_option: str  # "FREE" or "PAID"
    is_explicit: bool
    is_preview_only: bool

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'TrackMetadata':
        """Create TrackMetadata from API response."""
        return cls(
            id=data['id'],
            title=data['title'],
            main_artists=data.get('mainArtists', []),
            featured_artists=data.get('featuredArtists', []),
            bpm=data['bpm'],
            length=data['length'],
            moods=data.get('moods', []),
            genres=data.get('genres', []),
            images=data.get('images', {}),
            waveform_url=data.get('waveformUrl', ''),
            has_vocals=data.get('hasVocals', False),
            added=data.get('added', ''),
            tier_option=data.get('tierOption', 'FREE'),
            is_explicit=data.get('isExplicit', False),
            is_preview_only=data.get('isPreviewOnly', True)
        )


@dataclass
class SearchFilters:
    """Search and filter options for track queries."""
    term: Optional[str] = None
    genre: Optional[List[str]] = None
    mood: Optional[List[str]] = None
    bpm_min: Optional[int] = None
    bpm_max: Optional[int] = None
    has_vocals: Optional[bool] = None
    sort: str = "Relevance"  # Relevance, Date, Title
    order: str = "asc"  # asc, desc
    limit: int = 50
    offset: int = 0


# ============================================================================
# RETRY DECORATOR WITH EXPONENTIAL BACKOFF
# ============================================================================

def retry_with_backoff(max_retries: int = 5, initial_delay: float = 1.0):
    """
    Decorator for retrying requests with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except RateLimitError as e:
                    # For rate limits, wait until reset time
                    if e.reset_time:
                        logger.warning(f"Rate limit hit. Reset time: {e.reset_time}")
                        # Calculate wait time (simplified - just wait the delay)
                        time.sleep(delay)
                    raise
                except APIError as e:
                    last_exception = e
                    if e.status_code == 502:
                        # DDoS protection, use exponential backoff
                        if attempt < max_retries:
                            jitter = random.uniform(0, 1)
                            wait_time = delay * (2 ** attempt) + jitter
                            logger.warning(f"502 error, retrying in {wait_time:.2f}s (attempt {attempt + 1}/{max_retries})")
                            time.sleep(wait_time)
                        continue
                    elif e.status_code in [401, 403]:
                        # Don't retry authentication errors
                        raise
                    elif e.status_code >= 500:
                        # Server errors, retry with backoff
                        if attempt < max_retries:
                            jitter = random.uniform(0, 1)
                            wait_time = delay * (2 ** attempt) + jitter
                            logger.warning(f"Server error {e.status_code}, retrying in {wait_time:.2f}s")
                            time.sleep(wait_time)
                        continue
                    else:
                        # Other errors, don't retry
                        raise
                except requests.exceptions.RequestException as e:
                    last_exception = e
                    if attempt < max_retries:
                        jitter = random.uniform(0, 1)
                        wait_time = delay * (2 ** attempt) + jitter
                        logger.warning(f"Request exception, retrying in {wait_time:.2f}s: {str(e)}")
                        time.sleep(wait_time)
                    continue

            # If all retries failed, raise the last exception
            if last_exception:
                raise last_exception

        return wrapper
    return decorator


# ============================================================================
# CACHE MANAGER
# ============================================================================

class CacheManager:
    """Simple in-memory cache for search results and metadata."""

    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialize cache manager.

        Args:
            ttl_seconds: Time-to-live for cached items in seconds
        """
        self._cache: Dict[str, tuple[Any, datetime]] = {}
        self._ttl = timedelta(seconds=ttl_seconds)

    def get(self, key: str) -> Optional[Any]:
        """Get item from cache if not expired."""
        if key in self._cache:
            value, expires_at = self._cache[key]
            if datetime.utcnow() < expires_at:
                logger.debug(f"Cache hit: {key}")
                return value
            else:
                logger.debug(f"Cache expired: {key}")
                del self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """Set item in cache with TTL."""
        expires_at = datetime.utcnow() + self._ttl
        self._cache[key] = (value, expires_at)
        logger.debug(f"Cache set: {key}")

    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()
        logger.debug("Cache cleared")

    def cleanup_expired(self) -> None:
        """Remove expired items from cache."""
        now = datetime.utcnow()
        expired_keys = [k for k, (_, exp) in self._cache.items() if now >= exp]
        for key in expired_keys:
            del self._cache[key]
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache items")


# ============================================================================
# EPIDEMIC SOUND CLIENT
# ============================================================================

class EpidemicSoundClient:
    """
    Production-ready Epidemic Sound API Client.

    Supports:
    - Partner authentication flow
    - Track search with filters
    - Track download (MP3 320kbps)
    - Streaming (HLS)
    - Similar tracks recommendations
    - Rate limiting with exponential backoff
    - Caching layer
    - Comprehensive error handling

    Example:
        >>> client = EpidemicSoundClient(
        ...     access_key_id="your_key",
        ...     access_key_secret="your_secret"
        ... )
        >>> client.authenticate()
        >>> tracks = client.search_tracks(query="upbeat energetic", mood=["happy"])
        >>> client.download_track(tracks[0]['id'], "output.mp3")
    """

    BASE_URL = "https://partner-content-api.epidemicsound.com/v0"

    def __init__(
        self,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        user_id: str = "default-user",
        cache_ttl: int = 3600,
        session: Optional[requests.Session] = None
    ):
        """
        Initialize Epidemic Sound API client.

        Args:
            access_key_id: API access key ID (or set EPIDEMIC_SOUND_ACCESS_KEY_ID env var)
            access_key_secret: API access key secret (or set EPIDEMIC_SOUND_ACCESS_KEY_SECRET env var)
            user_id: Anonymized user identifier for token generation
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
            session: Optional requests.Session for connection pooling
        """
        # Get credentials from env if not provided
        self.access_key_id = access_key_id or os.getenv("EPIDEMIC_SOUND_ACCESS_KEY_ID")
        self.access_key_secret = access_key_secret or os.getenv("EPIDEMIC_SOUND_ACCESS_KEY_SECRET")

        if not self.access_key_id or not self.access_key_secret:
            raise ValueError(
                "API credentials not provided. Set EPIDEMIC_SOUND_ACCESS_KEY_ID and "
                "EPIDEMIC_SOUND_ACCESS_KEY_SECRET environment variables or pass to constructor."
            )

        self.user_id = user_id
        self._session = session or requests.Session()
        self._session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })

        # Token storage
        self._partner_token: Optional[TokenResponse] = None
        self._user_token: Optional[TokenResponse] = None

        # Cache manager
        self._cache = CacheManager(ttl_seconds=cache_ttl)

        logger.info("Epidemic Sound client initialized")

    # ========================================================================
    # AUTHENTICATION
    # ========================================================================

    @retry_with_backoff(max_retries=3)
    def _get_partner_token(self) -> TokenResponse:
        """
        Get partner token from API (Step 1 of authentication).

        Returns:
            TokenResponse with partner token

        Raises:
            AuthenticationError: If authentication fails
        """
        logger.info("Requesting partner token...")

        url = f"{self.BASE_URL}/partner-token"
        payload = {
            "accessKeyId": self.access_key_id,
            "accessKeySecret": self.access_key_secret
        }

        try:
            response = self._session.post(url, json=payload)

            if response.status_code == 200:
                data = response.json()
                token_response = TokenResponse(
                    token=data['token'],
                    expires_in=data['expiresIn']
                )
                logger.info("Partner token obtained successfully")
                return token_response
            else:
                raise AuthenticationError(
                    f"Failed to get partner token: {response.status_code} - {response.text}"
                )
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Network error getting partner token: {str(e)}")

    @retry_with_backoff(max_retries=3)
    def _get_user_token(self, partner_token: str) -> TokenResponse:
        """
        Get user token from API (Step 2 of authentication).

        Args:
            partner_token: Valid partner token

        Returns:
            TokenResponse with user token

        Raises:
            AuthenticationError: If authentication fails
        """
        logger.info(f"Requesting user token for user: {self.user_id}...")

        url = f"{self.BASE_URL}/token"
        payload = {"userId": self.user_id}
        headers = {"Authorization": f"Bearer {partner_token}"}

        try:
            response = self._session.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                token_response = TokenResponse(
                    token=data['token'],
                    expires_in=data['expiresIn']
                )
                logger.info("User token obtained successfully")
                return token_response
            else:
                raise AuthenticationError(
                    f"Failed to get user token: {response.status_code} - {response.text}"
                )
        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Network error getting user token: {str(e)}")

    def authenticate(self, force_refresh: bool = False) -> str:
        """
        Perform full authentication flow and return user token.

        Args:
            force_refresh: Force token refresh even if current token is valid

        Returns:
            Valid user token string

        Raises:
            AuthenticationError: If authentication fails
        """
        # Check if we have valid tokens
        if not force_refresh and self._user_token and not self._user_token.is_expired():
            logger.debug("Using cached user token")
            return self._user_token.token

        # Get partner token
        if not self._partner_token or self._partner_token.is_expired():
            self._partner_token = self._get_partner_token()

        # Get user token
        self._user_token = self._get_user_token(self._partner_token.token)

        return self._user_token.token

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get headers with valid authentication token."""
        token = self.authenticate()
        return {"Authorization": f"Bearer {token}"}

    # ========================================================================
    # REQUEST HELPERS
    # ========================================================================

    @retry_with_backoff(max_retries=5)
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        require_auth: bool = True
    ) -> Dict[str, Any]:
        """
        Make authenticated API request with error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (relative to BASE_URL)
            params: Query parameters
            json_data: JSON body data
            require_auth: Whether authentication is required

        Returns:
            Response JSON data

        Raises:
            APIError: For API errors
            RateLimitError: For rate limit errors
        """
        url = urljoin(self.BASE_URL + "/", endpoint)
        headers = self._get_auth_headers() if require_auth else {}

        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                headers=headers
            )

            # Check rate limit headers
            rate_limit_reached = response.headers.get('X-RateLimit-Reached', 'false').lower() == 'true'
            rate_limit_reset = response.headers.get('X-RateLimit-Reset')

            if rate_limit_reached:
                logger.warning(f"Rate limit reached. Reset at: {rate_limit_reset}")

            # Handle response
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 204:
                return {}
            elif response.status_code == 401:
                raise AuthenticationError("Authentication failed (401)")
            elif response.status_code == 403:
                raise APIError("Access forbidden (403) - may require subscription", 403, response.json())
            elif response.status_code == 429:
                raise RateLimitError(
                    "Rate limit exceeded (429)",
                    reset_time=rate_limit_reset
                )
            elif response.status_code == 400:
                error_data = response.json() if response.text else {}
                raise APIError(
                    f"Bad request (400): {error_data.get('error', {}).get('message', 'Invalid parameters')}",
                    400,
                    error_data
                )
            else:
                error_data = response.json() if response.text else {}
                raise APIError(
                    f"API error ({response.status_code}): {response.text}",
                    response.status_code,
                    error_data
                )
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    # ========================================================================
    # SEARCH & DISCOVERY
    # ========================================================================

    def search_tracks(
        self,
        query: Optional[str] = None,
        genre: Optional[List[str]] = None,
        mood: Optional[List[str]] = None,
        bpm_min: Optional[int] = None,
        bpm_max: Optional[int] = None,
        sort: str = "Relevance",
        order: str = "asc",
        limit: int = 50,
        offset: int = 0,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Search tracks with filters.

        Args:
            query: Search query text (semantic search supported)
            genre: List of genre IDs to filter by
            mood: List of mood IDs to filter by
            bpm_min: Minimum BPM threshold
            bpm_max: Maximum BPM threshold
            sort: Sort by "Relevance", "Date", or "Title"
            order: Sort order "asc" or "desc"
            limit: Results per page (max 60 for search)
            offset: Starting position for pagination
            use_cache: Whether to use cached results

        Returns:
            Dictionary with 'tracks', 'pagination', 'links', and 'aggregations'

        Example:
            >>> results = client.search_tracks(
            ...     query="upbeat energetic",
            ...     mood=["happy", "energetic"],
            ...     bpm_min=120,
            ...     bpm_max=140,
            ...     limit=25
            ... )
            >>> for track in results['tracks']:
            ...     print(f"{track['title']} - {track['bpm']} BPM")
        """
        # Build cache key
        cache_key = f"search:{query}:{genre}:{mood}:{bpm_min}:{bpm_max}:{sort}:{order}:{limit}:{offset}"

        if use_cache:
            cached = self._cache.get(cache_key)
            if cached:
                return cached

        # Build params
        params = {
            "limit": min(limit, 60),  # Max 60 for search endpoint
            "offset": offset,
            "sort": sort,
            "order": order
        }

        if query:
            params["term"] = query
        if genre:
            params["genre"] = genre if isinstance(genre, list) else [genre]
        if mood:
            params["mood"] = mood if isinstance(mood, list) else [mood]
        if bpm_min is not None:
            params["bpmMin"] = bpm_min
        if bpm_max is not None:
            params["bpmMax"] = bpm_max

        logger.info(f"Searching tracks with query: {query}, filters: genre={genre}, mood={mood}, BPM={bpm_min}-{bpm_max}")

        # Use search endpoint if query provided, otherwise use list endpoint
        endpoint = "tracks/search" if query else "tracks"

        result = self._make_request("GET", endpoint, params=params)

        if use_cache:
            self._cache.set(cache_key, result)

        logger.info(f"Found {len(result.get('tracks', []))} tracks")
        return result

    def get_track_metadata(self, track_id: str) -> TrackMetadata:
        """
        Get detailed metadata for a specific track.

        Args:
            track_id: Track identifier

        Returns:
            TrackMetadata object with full track details

        Example:
            >>> metadata = client.get_track_metadata("6rUPerw2po")
            >>> print(f"{metadata.title} - {metadata.bpm} BPM - {metadata.length}s")
        """
        # Search for track by ID (there's no direct get track endpoint)
        # We'll use the similar tracks endpoint which returns the original track
        logger.info(f"Getting metadata for track: {track_id}")

        # Try to get from similar endpoint which includes the track
        result = self._make_request("GET", f"tracks/{track_id}/similar", params={"limit": 1})

        if 'tracks' in result and len(result['tracks']) > 0:
            # The similar endpoint returns tracks, but we need the original
            # Let's search for it specifically
            search_result = self.search_tracks(query=track_id, limit=1)
            if search_result['tracks']:
                track_data = search_result['tracks'][0]
                return TrackMetadata.from_api_response(track_data)

        raise APIError(f"Track not found: {track_id}")

    def find_similar_tracks(
        self,
        track_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Find tracks similar to the given track.

        Args:
            track_id: Track identifier
            limit: Number of results (max varies by endpoint)
            offset: Starting position for pagination

        Returns:
            Dictionary with similar tracks

        Example:
            >>> similar = client.find_similar_tracks("6rUPerw2po", limit=10)
            >>> for track in similar['tracks']:
            ...     print(f"Similar: {track['title']}")
        """
        logger.info(f"Finding similar tracks for: {track_id}")

        params = {"limit": limit, "offset": offset}
        result = self._make_request("GET", f"tracks/{track_id}/similar", params=params)

        logger.info(f"Found {len(result.get('tracks', []))} similar tracks")
        return result

    def get_moods(
        self,
        type_filter: str = "all",
        sort: str = "relevance",
        order: str = "desc",
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Browse available moods.

        Args:
            type_filter: "all", "featured", or "partner-tier"
            sort: "alphabetic" or "relevance"
            order: "asc" or "desc"
            limit: Results per page (max 20)
            offset: Starting position

        Returns:
            Dictionary with moods list
        """
        params = {
            "type": type_filter,
            "sort": sort,
            "order": order,
            "limit": min(limit, 20),
            "offset": offset
        }

        return self._make_request("GET", "moods", params=params)

    def get_genres(
        self,
        type_filter: str = "all",
        sort: str = "relevance",
        order: str = "desc",
        limit: int = 20,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Browse available genres.

        Args:
            type_filter: "all", "featured", or "partner-tier"
            sort: "alphabetic" or "relevance"
            order: "asc" or "desc"
            limit: Results per page (max 20)
            offset: Starting position

        Returns:
            Dictionary with genres list
        """
        params = {
            "type": type_filter,
            "sort": sort,
            "order": order,
            "limit": min(limit, 20),
            "offset": offset
        }

        return self._make_request("GET", "genres", params=params)

    def get_collections(
        self,
        exclude_tracks: bool = False,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get curated collections (playlists).

        Args:
            exclude_tracks: Set True to exclude track data from response
            limit: Results per page (max 20)
            offset: Starting position

        Returns:
            Dictionary with collections list
        """
        params = {
            "limit": min(limit, 20),
            "offset": offset
        }

        if exclude_tracks:
            params["excludeField"] = "tracks"

        return self._make_request("GET", "collections", params=params)

    def get_suggestions(self, query: str) -> Dict[str, Any]:
        """
        Get autocomplete suggestions for search queries.

        Args:
            query: Partial search query

        Returns:
            Dictionary with suggestions
        """
        params = {"term": query}
        return self._make_request("GET", "tracks/suggestions", params=params)

    # ========================================================================
    # DOWNLOAD & STREAMING
    # ========================================================================

    def get_download_url(
        self,
        track_id: str,
        quality: str = "high"
    ) -> Dict[str, str]:
        """
        Get signed download URL for track.

        Args:
            track_id: Track identifier
            quality: "normal" (128kbps) or "high" (320kbps)

        Returns:
            Dictionary with 'url' and 'expires' fields

        Example:
            >>> download_info = client.get_download_url("6rUPerw2po", quality="high")
            >>> print(f"Download URL: {download_info['url']}")
            >>> print(f"Expires: {download_info['expires']}")
        """
        logger.info(f"Getting download URL for track: {track_id} (quality: {quality})")

        params = {
            "format": "mp3",
            "quality": quality
        }

        result = self._make_request("GET", f"tracks/{track_id}/download", params=params)

        logger.info(f"Download URL obtained, expires: {result.get('expires')}")
        return result

    @retry_with_backoff(max_retries=3)
    def download_track(
        self,
        track_id: str,
        output_path: Union[str, Path],
        quality: str = "high",
        chunk_size: int = 8192
    ) -> Path:
        """
        Download track to file.

        Args:
            track_id: Track identifier
            output_path: Path to save the MP3 file
            quality: "normal" (128kbps) or "high" (320kbps)
            chunk_size: Download chunk size in bytes

        Returns:
            Path to downloaded file

        Raises:
            DownloadError: If download fails

        Example:
            >>> client.download_track("6rUPerw2po", "music/track.mp3", quality="high")
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Get download URL
        download_info = self.get_download_url(track_id, quality)
        download_url = download_info['url']

        logger.info(f"Downloading track {track_id} to {output_path}")

        try:
            # Download file
            response = requests.get(download_url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            logger.debug(f"Download progress: {progress:.1f}%")

            logger.info(f"Download complete: {output_path} ({downloaded} bytes)")
            return output_path

        except Exception as e:
            raise DownloadError(f"Failed to download track {track_id}: {str(e)}")

    def batch_download(
        self,
        track_ids: List[str],
        output_dir: Union[str, Path],
        quality: str = "high",
        filename_template: str = "{track_id}.mp3"
    ) -> List[Path]:
        """
        Download multiple tracks to a directory.

        Args:
            track_ids: List of track identifiers
            output_dir: Directory to save tracks
            quality: "normal" or "high"
            filename_template: Template for filenames (can use {track_id}, {title}, {artist})

        Returns:
            List of paths to downloaded files

        Example:
            >>> tracks = ["track1", "track2", "track3"]
            >>> client.batch_download(tracks, "music/downloads/", quality="high")
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        downloaded_files = []
        total = len(track_ids)

        logger.info(f"Starting batch download of {total} tracks")

        for idx, track_id in enumerate(track_ids, 1):
            try:
                filename = filename_template.format(track_id=track_id)
                output_path = output_dir / filename

                logger.info(f"Downloading track {idx}/{total}: {track_id}")
                self.download_track(track_id, output_path, quality)
                downloaded_files.append(output_path)

                # Small delay to avoid rate limiting
                if idx < total:
                    time.sleep(0.5)

            except Exception as e:
                logger.error(f"Failed to download track {track_id}: {str(e)}")
                continue

        logger.info(f"Batch download complete: {len(downloaded_files)}/{total} successful")
        return downloaded_files

    def get_stream_url(self, track_id: str) -> Dict[str, str]:
        """
        Get HLS streaming URL for track.

        Args:
            track_id: Track identifier

        Returns:
            Dictionary with 'url' field containing HLS manifest URL

        Example:
            >>> stream_info = client.get_stream_url("6rUPerw2po")
            >>> print(f"Stream URL: {stream_info['url']}")
        """
        logger.info(f"Getting stream URL for track: {track_id}")
        result = self._make_request("GET", f"tracks/{track_id}/stream")
        return result

    # ========================================================================
    # ADVANCED FEATURES
    # ========================================================================

    def get_track_beats(self, track_id: str) -> Dict[str, Any]:
        """
        Get beat timestamp data for track synchronization.

        Args:
            track_id: Track identifier

        Returns:
            Dictionary with 'beats' array containing timestamp objects

        Example:
            >>> beats = client.get_track_beats("6rUPerw2po")
            >>> for beat in beats['beats'][:5]:
            ...     print(f"Beat at {beat['timestamp']}s")
        """
        logger.info(f"Getting beats for track: {track_id}")
        return self._make_request("GET", f"tracks/{track_id}/beats")

    def report_usage(
        self,
        track_id: str,
        platform: str = "youtube",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Report track usage to Epidemic Sound.

        Args:
            track_id: Track identifier
            platform: Platform name (youtube, tiktok, instagram, facebook, etc.)
            user_id: Optional user ID (defaults to client's user_id)

        Returns:
            Response data

        Example:
            >>> client.report_usage("6rUPerw2po", platform="youtube")
        """
        payload = {
            "trackId": track_id,
            "userId": user_id or self.user_id,
            "platform": platform,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        logger.info(f"Reporting usage for track {track_id} on {platform}")
        return self._make_request("POST", "usage", json_data=payload)

    def report_usage_bulk(self, events: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Report multiple usage events in bulk.

        Args:
            events: List of usage event dictionaries with trackId, userId, platform, timestamp

        Returns:
            Response data

        Example:
            >>> events = [
            ...     {"trackId": "track1", "userId": "user1", "platform": "youtube"},
            ...     {"trackId": "track2", "userId": "user1", "platform": "instagram"}
            ... ]
            >>> client.report_usage_bulk(events)
        """
        payload = {"events": events}
        logger.info(f"Reporting {len(events)} usage events in bulk")
        return self._make_request("POST", "usage/bulk", json_data=payload)

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def clear_cache(self) -> None:
        """Clear all cached search results."""
        self._cache.clear()
        logger.info("Cache cleared")

    def cleanup_cache(self) -> None:
        """Remove expired items from cache."""
        self._cache.cleanup_expired()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return {
            "total_items": len(self._cache._cache),
            "ttl_seconds": self._cache._ttl.total_seconds()
        }

    def close(self) -> None:
        """Close the HTTP session."""
        self._session.close()
        logger.info("Client session closed")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def create_client_from_env() -> EpidemicSoundClient:
    """
    Create client using environment variables.

    Required environment variables:
    - EPIDEMIC_SOUND_ACCESS_KEY_ID
    - EPIDEMIC_SOUND_ACCESS_KEY_SECRET

    Returns:
        Initialized EpidemicSoundClient

    Example:
        >>> client = create_client_from_env()
        >>> client.authenticate()
    """
    return EpidemicSoundClient()


def search_and_download(
    query: str,
    output_dir: Union[str, Path],
    limit: int = 5,
    quality: str = "high",
    **search_filters
) -> List[Path]:
    """
    Quick helper to search and download tracks.

    Args:
        query: Search query
        output_dir: Directory to save tracks
        limit: Number of tracks to download
        quality: Download quality
        **search_filters: Additional filters (genre, mood, bpm_min, bpm_max)

    Returns:
        List of downloaded file paths

    Example:
        >>> files = search_and_download(
        ...     "upbeat energetic",
        ...     "music/downloads/",
        ...     limit=3,
        ...     mood=["happy"],
        ...     bpm_min=120
        ... )
    """
    with create_client_from_env() as client:
        client.authenticate()

        # Search tracks
        results = client.search_tracks(query=query, limit=limit, **search_filters)
        tracks = results.get('tracks', [])

        if not tracks:
            logger.warning(f"No tracks found for query: {query}")
            return []

        # Download tracks
        track_ids = [track['id'] for track in tracks[:limit]]
        return client.batch_download(track_ids, output_dir, quality=quality)


# ============================================================================
# MAIN - EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    """
    Example usage of the Epidemic Sound client.

    Before running:
    1. Set environment variables:
       - EPIDEMIC_SOUND_ACCESS_KEY_ID
       - EPIDEMIC_SOUND_ACCESS_KEY_SECRET
    2. Or pass credentials directly to the client constructor
    """

    # Example 1: Basic usage with context manager
    print("=" * 80)
    print("EPIDEMIC SOUND API CLIENT - EXAMPLE USAGE")
    print("=" * 80)

    try:
        with EpidemicSoundClient() as client:
            # Authenticate
            print("\n[1] Authenticating...")
            client.authenticate()
            print("    Authentication successful!")

            # Search tracks
            print("\n[2] Searching for upbeat energetic music...")
            results = client.search_tracks(
                query="upbeat energetic workout",
                mood=["happy", "energetic"],
                bpm_min=120,
                bpm_max=140,
                limit=5
            )

            print(f"    Found {len(results['tracks'])} tracks:")
            for idx, track in enumerate(results['tracks'], 1):
                print(f"    {idx}. {track['title']} - {', '.join(track['mainArtists'])}")
                print(f"       BPM: {track['bpm']}, Duration: {track['length']}s, Vocals: {track['hasVocals']}")

            # Get similar tracks
            if results['tracks']:
                first_track = results['tracks'][0]
                print(f"\n[3] Finding tracks similar to '{first_track['title']}'...")
                similar = client.find_similar_tracks(first_track['id'], limit=3)

                print(f"    Found {len(similar.get('tracks', []))} similar tracks:")
                for idx, track in enumerate(similar.get('tracks', []), 1):
                    print(f"    {idx}. {track['title']} - {', '.join(track['mainArtists'])}")

            # Get download URL (don't actually download in example)
            if results['tracks']:
                track_id = results['tracks'][0]['id']
                print(f"\n[4] Getting download URL for track: {track_id}")
                download_info = client.get_download_url(track_id, quality="high")
                print(f"    Download URL obtained (expires: {download_info['expires']})")
                print(f"    URL: {download_info['url'][:100]}...")

            # Browse moods and genres
            print("\n[5] Browsing available moods...")
            moods = client.get_moods(type_filter="featured", limit=5)
            print(f"    Featured moods:")
            for mood in moods.get('moods', [])[:5]:
                print(f"    - {mood['name']} (ID: {mood['id']})")

            print("\n[6] Browsing available genres...")
            genres = client.get_genres(type_filter="featured", limit=5)
            print(f"    Featured genres:")
            for genre in genres.get('genres', [])[:5]:
                print(f"    - {genre['name']} (ID: {genre['id']})")

            # Cache stats
            print("\n[7] Cache statistics:")
            stats = client.get_cache_stats()
            print(f"    Cached items: {stats['total_items']}")
            print(f"    Cache TTL: {stats['ttl_seconds']}s")

    except AuthenticationError as e:
        print(f"\n❌ Authentication failed: {e}")
        print("\nMake sure to set environment variables:")
        print("  - EPIDEMIC_SOUND_ACCESS_KEY_ID")
        print("  - EPIDEMIC_SOUND_ACCESS_KEY_SECRET")
    except APIError as e:
        print(f"\n❌ API error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 80)
    print("Example complete!")
    print("=" * 80)
