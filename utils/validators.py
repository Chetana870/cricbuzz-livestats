"""
Validation helpers — used by crud_service before any INSERT/UPDATE hits the DB.
Keeping validation separate from the SQL logic makes both easier to test
and means bad data never even reaches a database call.
"""

VALID_PLAYING_ROLES = {"Batsman", "Bowler", "All-rounder", "Wicket-keeper"}


class ValidationError(Exception):
    """Raised when input data fails validation, before any DB call is made."""
    pass


def validate_player_data(full_name: str, country: str, playing_role: str, team_id: int = None):
    """
    Validates a player's data before insert/update.
    Raises ValidationError with a clear message if anything is invalid.
    """
    if not full_name or not full_name.strip():
        raise ValidationError("Player name cannot be empty.")

    if len(full_name) > 150:
        raise ValidationError("Player name is too long (max 150 characters).")

    if not country or not country.strip():
        raise ValidationError("Country cannot be empty.")

    if playing_role not in VALID_PLAYING_ROLES:
        raise ValidationError(
            f"playing_role must be one of {VALID_PLAYING_ROLES}, got '{playing_role}'."
        )

    if team_id is not None and (not isinstance(team_id, int) or team_id <= 0):
        raise ValidationError("team_id must be a positive integer.")


def validate_player_id(player_id) -> int:
    """Ensures a player_id is a usable positive integer before a lookup/update/delete."""
    try:
        player_id = int(player_id)
    except (TypeError, ValueError):
        raise ValidationError("player_id must be a number.")
    if player_id <= 0:
        raise ValidationError("player_id must be a positive integer.")
    return player_id


def validate_team_data(team_name: str, country: str):
    """Validates a team's data before insert/update."""
    if not team_name or not team_name.strip():
        raise ValidationError("Team name cannot be empty.")
    if len(team_name) > 100:
        raise ValidationError("Team name is too long (max 100 characters).")
    if not country or not country.strip():
        raise ValidationError("Country cannot be empty.")


def validate_team_id(team_id) -> int:
    """Ensures a team_id is a usable positive integer before a lookup/update/delete."""
    try:
        team_id = int(team_id)
    except (TypeError, ValueError):
        raise ValidationError("team_id must be a number.")
    if team_id <= 0:
        raise ValidationError("team_id must be a positive integer.")
    return team_id
