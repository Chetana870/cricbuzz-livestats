"""
CRUD service for the players table.

Every function here:
  1. Validates input (via utils.validators) BEFORE touching the database
  2. Uses parameterized queries (never string-formatted SQL) to prevent SQL injection
  3. Relies on database.db_connection.get_cursor() for automatic commit/rollback

This is the plain-Python layer. Streamlit pages (Phase 12) will call these
functions directly — no SQL or psycopg2 code should ever live in a page file.
"""

import logging
from database.db_connection import get_cursor
from utils.validators import (
    validate_player_data, validate_player_id,
    validate_team_data, validate_team_id,
    ValidationError,
)

logger = logging.getLogger(__name__)


def create_player(full_name: str, country: str, playing_role: str,
                   batting_style: str = None, bowling_style: str = None,
                   team_id: int = None) -> dict:
    """
    Insert a new player. Returns the newly created row as a dict.
    Raises ValidationError on bad input, psycopg2 errors on DB failure.
    """
    validate_player_data(full_name, country, playing_role, team_id)

    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            INSERT INTO players (full_name, country, playing_role, batting_style, bowling_style, team_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING player_id, full_name, country, playing_role, batting_style, bowling_style, team_id
            """,
            (full_name, country, playing_role, batting_style, bowling_style, team_id),
        )
        row = cur.fetchone()
        logger.info(f"Created player: {row['full_name']} (id={row['player_id']})")
        return dict(row)


def get_player(player_id: int) -> dict | None:
    """Fetch a single player by ID. Returns None if not found."""
    player_id = validate_player_id(player_id)

    with get_cursor() as cur:
        cur.execute("SELECT * FROM players WHERE player_id = %s", (player_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def list_players(country: str = None, playing_role: str = None) -> list[dict]:
    """
    List all players, optionally filtered by country and/or playing_role.
    Used to populate the CRUD page's table view.
    """
    query = "SELECT * FROM players WHERE 1=1"
    params = []

    if country:
        query += " AND country = %s"
        params.append(country)
    if playing_role:
        query += " AND playing_role = %s"
        params.append(playing_role)

    query += " ORDER BY full_name"

    with get_cursor() as cur:
        cur.execute(query, tuple(params))
        return [dict(row) for row in cur.fetchall()]


def update_player(player_id: int, full_name: str, country: str, playing_role: str,
                   batting_style: str = None, bowling_style: str = None,
                   team_id: int = None) -> dict | None:
    """
    Update an existing player's data. Returns the updated row, or None if
    the player_id doesn't exist.
    """
    player_id = validate_player_id(player_id)
    validate_player_data(full_name, country, playing_role, team_id)

    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            UPDATE players
            SET full_name = %s, country = %s, playing_role = %s,
                batting_style = %s, bowling_style = %s, team_id = %s
            WHERE player_id = %s
            RETURNING player_id, full_name, country, playing_role, batting_style, bowling_style, team_id
            """,
            (full_name, country, playing_role, batting_style, bowling_style, team_id, player_id),
        )
        row = cur.fetchone()
        if row:
            logger.info(f"Updated player id={player_id}")
            return dict(row)
        logger.warning(f"Update failed — no player with id={player_id}")
        return None


def delete_player(player_id: int) -> bool:
    """
    Delete a player by ID. Returns True if a row was deleted, False if
    the player_id didn't exist.

    Note: this will fail with a foreign key violation if the player has
    existing batting/bowling/fielding performance rows — that's intentional,
    it protects historical match data from accidental deletion.
    """
    player_id = validate_player_id(player_id)

    with get_cursor(commit=True) as cur:
        cur.execute("DELETE FROM players WHERE player_id = %s", (player_id,))
        deleted = cur.rowcount > 0
        if deleted:
            logger.info(f"Deleted player id={player_id}")
        else:
            logger.warning(f"Delete failed — no player with id={player_id}")
        return deleted


# ---------------------------------------------------------------------------
# Teams CRUD
# ---------------------------------------------------------------------------

def create_team(team_name: str, country: str) -> dict:
    """Insert a new team. Returns the newly created row as a dict."""
    validate_team_data(team_name, country)

    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            INSERT INTO teams (team_name, country)
            VALUES (%s, %s)
            RETURNING team_id, team_name, country
            """,
            (team_name, country),
        )
        row = cur.fetchone()
        logger.info(f"Created team: {row['team_name']} (id={row['team_id']})")
        return dict(row)


def get_team(team_id: int) -> dict | None:
    """Fetch a single team by ID. Returns None if not found."""
    team_id = validate_team_id(team_id)
    with get_cursor() as cur:
        cur.execute("SELECT * FROM teams WHERE team_id = %s", (team_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def list_teams() -> list[dict]:
    """List all teams, ordered by name. Also used to populate dropdowns for player forms."""
    with get_cursor() as cur:
        cur.execute("SELECT * FROM teams ORDER BY team_name")
        return [dict(row) for row in cur.fetchall()]


def update_team(team_id: int, team_name: str, country: str) -> dict | None:
    """Update an existing team. Returns the updated row, or None if not found."""
    team_id = validate_team_id(team_id)
    validate_team_data(team_name, country)

    with get_cursor(commit=True) as cur:
        cur.execute(
            """
            UPDATE teams SET team_name = %s, country = %s
            WHERE team_id = %s
            RETURNING team_id, team_name, country
            """,
            (team_name, country, team_id),
        )
        row = cur.fetchone()
        if row:
            logger.info(f"Updated team id={team_id}")
            return dict(row)
        logger.warning(f"Update failed — no team with id={team_id}")
        return None


def delete_team(team_id: int) -> bool:
    """
    Delete a team by ID. Returns True if deleted, False if not found.
    Will fail with a foreign key violation if players or matches still
    reference this team — intentional, protects existing data.
    """
    team_id = validate_team_id(team_id)
    with get_cursor(commit=True) as cur:
        cur.execute("DELETE FROM teams WHERE team_id = %s", (team_id,))
        deleted = cur.rowcount > 0
        if deleted:
            logger.info(f"Deleted team id={team_id}")
        else:
            logger.warning(f"Delete failed — no team with id={team_id}")
        return deleted
