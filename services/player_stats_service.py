"""
Player stats service — two distinct data sources:
  1. Live ICC-style rankings from the Cricbuzz API (get_live_rankings)
  2. Our own database leaderboards, built from stored match data (get_db_leaderboard)
"""

import logging
from api.cricbuzz_client import get_batsmen_rankings, get_bowlers_rankings, CricbuzzAPIError
from database.db_connection import get_cursor

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Live API rankings
# ---------------------------------------------------------------------------

def _flatten_rankings(raw_response: dict) -> list[dict]:
    """
    Flattens the rankings API response into a simple list of dicts.
    Defensive against missing keys since the exact shape can vary by provider.
    """
    flattened = []
    rankings = raw_response.get("rank", []) or raw_response.get("rankings", [])

    for entry in rankings:
        flattened.append({
            "rank": entry.get("rank"),
            "player_name": entry.get("name", "Unknown"),
            "country": entry.get("country", ""),
            "rating": entry.get("rating", ""),
        })

    return flattened


def get_live_batting_rankings(format_type: str = "test") -> list[dict]:
    """Currently ranked top batsmen from the API. Empty list on failure."""
    try:
        raw = get_batsmen_rankings(format_type)
        return _flatten_rankings(raw)
    except CricbuzzAPIError as e:
        logger.error(f"Failed to fetch batting rankings: {e}")
        return []


def get_live_bowling_rankings(format_type: str = "test") -> list[dict]:
    """Currently ranked top bowlers from the API. Empty list on failure."""
    try:
        raw = get_bowlers_rankings(format_type)
        return _flatten_rankings(raw)
    except CricbuzzAPIError as e:
        logger.error(f"Failed to fetch bowling rankings: {e}")
        return []


# ---------------------------------------------------------------------------
# Database leaderboards (reuses the logic from Phase 11, Q3 and Q11)
# Now with optional country filter and adjustable limit for interactivity.
# ---------------------------------------------------------------------------

def get_all_countries() -> list[str]:
    """Distinct list of player countries, used to populate the filter dropdown."""
    with get_cursor() as cur:
        cur.execute("SELECT DISTINCT country FROM players ORDER BY country")
        return [row["country"] for row in cur.fetchall()]


def get_top_run_scorers(limit: int = 10, country: str = None) -> list[dict]:
    """Top run-scorers from our own stored match data (Phase 11, Question 3)."""
    query = """
        SELECT
            p.player_id,
            p.full_name,
            p.country,
            COUNT(bp.match_id) AS innings_played,
            SUM(bp.runs_scored) AS total_runs,
            ROUND(AVG(bp.runs_scored), 2) AS batting_average,
            MAX(bp.runs_scored) AS highest_score
        FROM players p
        JOIN batting_performances bp ON p.player_id = bp.player_id
        WHERE 1=1
    """
    params = []
    if country:
        query += " AND p.country = %s"
        params.append(country)

    query += """
        GROUP BY p.player_id, p.full_name, p.country
        ORDER BY total_runs DESC
        LIMIT %s
    """
    params.append(limit)

    with get_cursor() as cur:
        cur.execute(query, tuple(params))
        return [dict(row) for row in cur.fetchall()]


def get_top_wicket_takers(limit: int = 10, country: str = None) -> list[dict]:
    """Top wicket-takers from our own stored match data (Phase 11, Question 11 style)."""
    query = """
        SELECT
            p.player_id,
            p.full_name,
            p.country,
            COUNT(bp.match_id) AS innings_bowled,
            SUM(bp.wickets_taken) AS total_wickets,
            ROUND(AVG(bp.economy_rate), 2) AS avg_economy
        FROM players p
        JOIN bowling_performances bp ON p.player_id = bp.player_id
        WHERE 1=1
    """
    params = []
    if country:
        query += " AND p.country = %s"
        params.append(country)

    query += """
        GROUP BY p.player_id, p.full_name, p.country
        ORDER BY total_wickets DESC
        LIMIT %s
    """
    params.append(limit)

    with get_cursor() as cur:
        cur.execute(query, tuple(params))
        return [dict(row) for row in cur.fetchall()]


def get_player_batting_history(player_id: int) -> list[dict]:
    """Every batting performance for one player, match by match — used for drill-down."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                m.match_description,
                m.match_format,
                m.match_date,
                bp.runs_scored,
                bp.balls_faced,
                bp.strike_rate,
                bp.is_out,
                bp.dismissal_type
            FROM batting_performances bp
            JOIN matches m ON bp.match_id = m.match_id
            WHERE bp.player_id = %s
            ORDER BY m.match_date DESC
            """,
            (player_id,),
        )
        return [dict(row) for row in cur.fetchall()]


def get_player_bowling_history(player_id: int) -> list[dict]:
    """Every bowling performance for one player, match by match — used for drill-down."""
    with get_cursor() as cur:
        cur.execute(
            """
            SELECT
                m.match_description,
                m.match_format,
                m.match_date,
                bp.overs_bowled,
                bp.runs_conceded,
                bp.wickets_taken,
                bp.economy_rate
            FROM bowling_performances bp
            JOIN matches m ON bp.match_id = m.match_id
            WHERE bp.player_id = %s
            ORDER BY m.match_date DESC
            """,
            (player_id,),
        )
        return [dict(row) for row in cur.fetchall()]