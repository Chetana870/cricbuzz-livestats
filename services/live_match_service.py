"""
Live match service — fetches from the Cricbuzz API and flattens the
deeply nested JSON response into a simple list of dicts the UI can loop over.

Pages should call parse functions here, never touch the raw API JSON directly.
"""

import logging
from api.cricbuzz_client import get_live_matches, get_recent_matches, CricbuzzAPIError

logger = logging.getLogger(__name__)


def _flatten_matches(raw_response: dict) -> list[dict]:
    """
    Walks typeMatches -> seriesMatches -> seriesAdWrapper -> matches
    and returns a flat list of simplified match dicts.

    Defensive against missing keys, since live API responses can vary
    in shape (e.g. a series with no matches currently live).
    """
    flattened = []

    for type_match in raw_response.get("typeMatches", []):
        for series_match in type_match.get("seriesMatches", []):
            wrapper = series_match.get("seriesAdWrapper")
            if not wrapper:
                continue

            series_name = wrapper.get("seriesName", "Unknown Series")

            for match in wrapper.get("matches", []):
                info = match.get("matchInfo", {})
                score = match.get("matchScore", {})

                team1_name = info.get("team1", {}).get("teamName", "TBD")
                team2_name = info.get("team2", {}).get("teamName", "TBD")

                flattened.append({
                    "match_id": info.get("matchId"),
                    "series_name": series_name,
                    "match_desc": info.get("matchDesc", ""),
                    "match_format": info.get("matchFormat", ""),
                    "team1": team1_name,
                    "team2": team2_name,
                    "status": info.get("status", "Status unavailable"),
                    "venue": info.get("venueInfo", {}).get("ground", "Unknown venue"),
                    "raw_score": score,
                })

    return flattened


def get_live_matches_flat() -> list[dict]:
    """Returns currently live matches, flattened and simplified. Empty list on failure."""
    try:
        raw = get_live_matches()
        return _flatten_matches(raw)
    except CricbuzzAPIError as e:
        logger.error(f"Failed to fetch live matches: {e}")
        return []


def get_recent_matches_flat() -> list[dict]:
    """Returns recent matches, flattened and simplified. Empty list on failure."""
    try:
        raw = get_recent_matches()
        return _flatten_matches(raw)
    except CricbuzzAPIError as e:
        logger.error(f"Failed to fetch recent matches: {e}")
        return []


def get_scorecard_flat(match_id: int) -> dict:
    """
    Fetches and lightly flattens a match scorecard for display.
    Returns a dict with 'innings': a list of {inning_label, batting: [...], bowling: [...]}.
    Defensive against shape variation since scorecard responses are complex.
    """
    from api.cricbuzz_client import get_match_scorecard

    try:
        raw = get_match_scorecard(match_id)
    except CricbuzzAPIError as e:
        logger.error(f"Failed to fetch scorecard for match {match_id}: {e}")
        return {"innings": [], "error": str(e)}

    innings_list = []
    for innings in raw.get("scorecard", []):
        batsmen = []
        for player in innings.get("batsman", []):
            batsmen.append({
                "batsman": player.get("name", "Unknown"),
                "runs": player.get("runs", 0),
                "balls": player.get("balls", 0),
                "fours": player.get("fours", 0),
                "sixes": player.get("sixes", 0),
                "dismissal": player.get("outdec", "not out"),
            })

        bowlers = []
        for player in innings.get("bowler", []):
            bowlers.append({
                "bowler": player.get("name", "Unknown"),
                "overs": player.get("overs", 0),
                "runs": player.get("runs", 0),
                "wickets": player.get("wickets", 0),
                "economy": player.get("economyrate", player.get("economy", 0)),
            })

        innings_list.append({
            "inning_label": f"Innings {innings.get('inningsid', len(innings_list) + 1)}",
            "batting": batsmen,
            "bowling": bowlers,
        })

    return {"innings": innings_list, "error": None}
