"""
Manual CRUD test — run this to confirm create/read/update/delete all work
against your real database before wiring up the Streamlit UI.

    python -m data.test_crud_manually
"""

from services.crud_service import create_player, get_player, list_players, update_player, delete_player
from utils.validators import ValidationError

if __name__ == "__main__":
    print("1. Creating a test player...")
    new_player = create_player(
        full_name="Test Player",
        country="India",
        playing_role="All-rounder",
        batting_style="Left-hand bat",
        bowling_style="Left-arm orthodox",
        team_id=1,
    )
    print(f"   Created: {new_player}\n")

    player_id = new_player["player_id"]

    print(f"2. Reading player id={player_id}...")
    fetched = get_player(player_id)
    print(f"   Fetched: {fetched}\n")

    print("3. Listing all players from India...")
    india_players = list_players(country="India")
    print(f"   Found {len(india_players)} player(s)\n")

    print(f"4. Updating player id={player_id}...")
    updated = update_player(
        player_id, full_name="Test Player Updated", country="India",
        playing_role="Bowler", team_id=1,
    )
    print(f"   Updated: {updated}\n")

    print("5. Testing validation (should fail cleanly)...")
    try:
        create_player(full_name="", country="India", playing_role="Batsman")
    except ValidationError as e:
        print(f"   Correctly rejected: {e}\n")

    print(f"6. Deleting player id={player_id}...")
    deleted = delete_player(player_id)
    print(f"   Deleted: {deleted}\n")

    print(f"7. Confirming deletion...")
    confirm = get_player(player_id)
    print(f"   Player now: {confirm} (should be None)")
