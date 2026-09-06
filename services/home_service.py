"""
Home page service — quick summary counts pulled from the database,
plus a simple player search used for the Home page's quick-search box.
"""

import logging
from database.db_connection import get_cursor

logger = logging.getLogger(__name__)


def get_summary_counts() -> dict:
    """Returns total counts of teams, players, matches, series for the Home dashboard."""
    try:
        with get_cursor() as cur:
            cur.execute("SELECT COUNT(*) AS count FROM teams")
            teams = cur.fetchone()["count"]

            cur.execute("SELECT COUNT(*) AS count FROM players")
            players = cur.fetchone()["count"]

            cur.execute("SELECT COUNT(*) AS count FROM matches")
            matches = cur.fetchone()["count"]

            cur.execute("SELECT COUNT(*) AS count FROM series")
            series = cur.fetchone()["count"]

        return {"teams": teams, "players": players, "matches": matches, "series": series}
    except Exception as e:
        logger.error(f"Failed to fetch summary counts: {e}")
        return {"teams": 0, "players": 0, "matches": 0, "series": 0}


def search_players(search_term: str) -> list[dict]:
    """Case-insensitive partial match search on player name, for Home's quick search."""
    if not search_term or not search_term.strip():
        return []

    try:
        with get_cursor() as cur:
            cur.execute(
                """
                SELECT p.full_name, p.country, p.playing_role, t.team_name
                FROM players p
                LEFT JOIN teams t ON p.team_id = t.team_id
                WHERE p.full_name ILIKE %s
                ORDER BY p.full_name
                LIMIT 10
                """,
                (f"%{search_term}%",),
            )
            return [dict(row) for row in cur.fetchall()]
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []