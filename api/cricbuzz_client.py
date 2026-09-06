"""
Cricbuzz API client — the ONLY place in this project that calls requests.get()
against the Cricbuzz API. Every other module goes through here.

If your RapidAPI dashboard shows different endpoint paths than the ones below,
update BASE_URL / the endpoint constants — nothing else needs to change.
"""

import time
import logging
import requests

from config import RAPIDAPI_KEY, RAPIDAPI_HOST

logger = logging.getLogger(__name__)

BASE_URL = f"https://{RAPIDAPI_HOST}"
HEADERS = {
    "X-RapidAPI-Host": RAPIDAPI_HOST,
    "X-RapidAPI-Key": RAPIDAPI_KEY,
}

MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2
TIMEOUT_SECONDS = 10


class CricbuzzAPIError(Exception):
    """Raised when the Cricbuzz API returns an error we can't recover from."""
    pass


def _get(endpoint: str, params: dict = None) -> dict:
    """
    Internal helper: performs a GET request with retry/backoff.
    All public functions below call this instead of requests.get() directly.
    """
    url = f"{BASE_URL}{endpoint}"
    last_exception = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            status = response.status_code
            if status == 401:
                # Bad/missing API key — retrying won't help
                logger.error("401 Unauthorized — check RAPIDAPI_KEY in .env")
                raise CricbuzzAPIError("Invalid or missing RapidAPI key") from e
            if status == 404:
                logger.error(f"404 Not Found — endpoint may not exist on your plan: {endpoint}")
                raise CricbuzzAPIError(f"Endpoint not found: {endpoint}") from e
            if status == 429:
                logger.warning(f"429 Rate limited on attempt {attempt}, backing off...")
                last_exception = e
                time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                continue
            logger.warning(f"HTTP error {status} on attempt {attempt}: {e}")
            last_exception = e

        except requests.exceptions.ConnectionError as e:
            logger.warning(f"Connection error on attempt {attempt}: {e}")
            last_exception = e
            time.sleep(RETRY_BACKOFF_SECONDS * attempt)

        except requests.exceptions.Timeout as e:
            logger.warning(f"Timeout on attempt {attempt}: {e}")
            last_exception = e
            time.sleep(RETRY_BACKOFF_SECONDS * attempt)

        except ValueError as e:
            # response.json() failed — response wasn't valid JSON
            logger.error(f"Invalid JSON response from {endpoint}: {e}")
            raise CricbuzzAPIError(f"Invalid JSON from {endpoint}") from e

    raise CricbuzzAPIError(f"Failed after {MAX_RETRIES} attempts: {last_exception}")


# ---------------------------------------------------------------------------
# Public functions — one per endpoint. Confirm these paths match your
# RapidAPI "Endpoints" tab; adjust the string if yours differs.
# ---------------------------------------------------------------------------

def get_recent_matches() -> dict:
    """Recent matches across all series."""
    return _get("/matches/v1/recent")


def get_live_matches() -> dict:
    """Currently live matches."""
    return _get("/matches/v1/live")


def get_upcoming_matches() -> dict:
    """Scheduled upcoming matches."""
    return _get("/matches/v1/upcoming")


def get_match_scorecard(match_id: int) -> dict:
    """Full scorecard (batting/bowling per innings) for a specific match."""
    return _get(f"/mcenter/v1/{match_id}/scard")


def get_series_info(series_id: int) -> dict:
    """Series details including teams and matches."""
    return _get(f"/series/v1/{series_id}")


def get_player_stats(player_id: int) -> dict:
    """Player profile and career stats."""
    return _get(f"/stats/v1/player/{player_id}")

def get_batsmen_rankings(format_type: str = "test") -> dict:
    """
    ICC-style batting rankings. format_type is typically 'test', 'odi', or 't20'
    depending on what your RapidAPI dashboard's Endpoints tab shows.
    """
    return _get(f"/stats/v1/rankings/batsmen", params={"formatType": format_type})


def get_bowlers_rankings(format_type: str = "test") -> dict:
    """ICC-style bowling rankings."""
    return _get(f"/stats/v1/rankings/bowlers", params={"formatType": format_type})
