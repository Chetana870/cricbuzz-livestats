"""
One-off manual test — NOT part of the pytest suite (that comes in Phase 15).
Run this to confirm your RAPIDAPI_KEY actually works before building on top of it.

    python -m data.test_api_manually
"""

from api.cricbuzz_client import get_recent_matches, CricbuzzAPIError
import json

if __name__ == "__main__":
    try:
        data = get_recent_matches()
        print("SUCCESS — API responded. First 500 chars of response:\n")
        print(json.dumps(data, indent=2)[:500])
    except CricbuzzAPIError as e:
        print(f"API call failed: {e}")
