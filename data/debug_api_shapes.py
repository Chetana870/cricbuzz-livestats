"""
Debug script — prints the real JSON structure from your API so we can
fix the parsing code to match your actual provider's response shape.

    python -m data.debug_api_shapes
"""

import json
from api.cricbuzz_client import get_recent_matches, get_match_scorecard

if __name__ == "__main__":
    print("=" * 60)
    print("STEP 1: Checking match_format values from recent matches")
    print("=" * 60)
    raw = get_recent_matches()
    match_id_to_test = None

    for type_match in raw.get("typeMatches", []):
        for series_match in type_match.get("seriesMatches", []):
            wrapper = series_match.get("seriesAdWrapper")
            if not wrapper:
                continue
            for match in wrapper.get("matches", []):
                info = match.get("matchInfo", {})
                print(f"  matchFormat = '{info.get('matchFormat')}'  (matchId={info.get('matchId')})")
                if match_id_to_test is None:
                    match_id_to_test = info.get("matchId")

    print()
    print("=" * 60)
    print(f"STEP 2: Fetching scorecard for matchId={match_id_to_test}")
    print("=" * 60)

    if match_id_to_test:
        scorecard_raw = get_match_scorecard(match_id_to_test)
        print("Top-level keys in scorecard response:")
        print(list(scorecard_raw.keys()))
        print()
        print("Full response (first 2000 chars):")
        print(json.dumps(scorecard_raw, indent=2)[:2000])
    else:
        print("No match_id found to test scorecard endpoint.")