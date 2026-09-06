"""
Analytics service — centralizes all SQL Analytics questions in one place.

Each entry has a title, business-problem description, the SQL itself, and
optional params the query needs. The Streamlit page just picks one and runs it.

Only Questions 1-14 (confirmed and tested in Phase 11) are included here.
Add Q15-25 the same way once they're written and validated.
"""

from database.db_connection import get_cursor

QUERIES = {
    1: {
        "title": "Q1: All players and their teams",
        "description": "Every player alongside their team name and country.",
        "sql": """
            SELECT p.full_name, p.playing_role, t.team_name, t.country
            FROM players p
            JOIN teams t ON p.team_id = t.team_id
            ORDER BY t.team_name, p.full_name;
        """,
    },
    2: {
        "title": "Q2: Recent matches with team and venue details",
        "description": "Matches with both team names and venue info, most recent first.",
        "sql": """
            SELECT m.match_id, m.match_description, m.match_format,
                   t1.team_name AS team1, t2.team_name AS team2,
                   v.venue_name, v.city, m.match_date
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            WHERE m.match_date >= '2024-01-01'
            ORDER BY m.match_date DESC;
        """,
    },
    3: {
        "title": "Q3: Top run scorers",
        "description": "Top 10 players by total runs scored across all stored matches.",
        "sql": """
            SELECT p.full_name, p.country,
                   COUNT(bp.match_id) AS innings_played,
                   SUM(bp.runs_scored) AS total_runs,
                   ROUND(AVG(bp.runs_scored), 2) AS batting_average,
                   MAX(bp.runs_scored) AS highest_score
            FROM players p
            JOIN batting_performances bp ON p.player_id = bp.player_id
            GROUP BY p.player_id, p.full_name, p.country
            ORDER BY total_runs DESC
            LIMIT 10;
        """,
    },
    4: {
        "title": "Q4: Best individual bowling performances",
        "description": "Top 10 single-match bowling figures, ranked by wickets then economy.",
        "sql": """
            SELECT p.full_name AS bowler, t.team_name AS bowler_team,
                   m.match_description, m.match_date,
                   bp.overs_bowled, bp.runs_conceded, bp.wickets_taken, bp.economy_rate
            FROM bowling_performances bp
            JOIN players p ON bp.player_id = p.player_id
            JOIN teams t ON bp.team_id = t.team_id
            JOIN matches m ON bp.match_id = m.match_id
            ORDER BY bp.wickets_taken DESC, bp.runs_conceded ASC
            LIMIT 10;
        """,
    },
    5: {
        "title": "Q5: Team win counts",
        "description": "How many matches each team has won (includes teams with zero wins).",
        "sql": """
            SELECT t.team_name, COUNT(m.match_id) AS matches_won
            FROM teams t
            LEFT JOIN matches m ON t.team_id = m.winner_team_id
            GROUP BY t.team_id, t.team_name
            ORDER BY matches_won DESC;
        """,
    },
    6: {
        "title": "Q6: Batting performance by format",
        "description": "Each player's runs and average, broken down by Test/ODI/T20 format.",
        "sql": """
            SELECT p.full_name, m.match_format,
                   COUNT(bp.match_id) AS innings_played,
                   SUM(bp.runs_scored) AS total_runs,
                   ROUND(AVG(bp.runs_scored), 2) AS avg_runs
            FROM players p
            JOIN batting_performances bp ON p.player_id = bp.player_id
            JOIN matches m ON bp.match_id = m.match_id
            GROUP BY p.player_id, p.full_name, m.match_format
            ORDER BY p.full_name, m.match_format;
        """,
    },
    7: {
        "title": "Q7: Home vs away wins per team",
        "description": "Each team's wins split by whether the venue's country matched their own.",
        "sql": """
            SELECT t.team_name,
                   COUNT(*) AS total_wins,
                   COUNT(*) FILTER (WHERE t.country = v.country) AS home_wins,
                   COUNT(*) FILTER (WHERE t.country != v.country) AS away_wins
            FROM matches m
            JOIN teams t ON m.winner_team_id = t.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            GROUP BY t.team_id, t.team_name
            ORDER BY total_wins DESC;
        """,
    },
    8: {
        "title": "Q8: Average winning margin by venue",
        "description": "Average victory margin at each venue, split by runs vs wickets.",
        "sql": """
            SELECT v.venue_name, v.city, m.victory_type,
                   COUNT(*) AS matches_with_this_margin_type,
                   ROUND(AVG(m.victory_margin), 1) AS avg_margin
            FROM matches m
            JOIN venues v ON m.venue_id = v.venue_id
            WHERE m.victory_margin IS NOT NULL
            GROUP BY v.venue_id, v.venue_name, v.city, m.victory_type
            ORDER BY v.venue_name, m.victory_type;
        """,
    },
    9: {
        "title": "Q9: Above-average batters",
        "description": "Players whose average runs per innings exceeds the overall average.",
        "sql": """
            SELECT p.full_name, ROUND(AVG(bp.runs_scored), 2) AS player_avg_runs
            FROM players p
            JOIN batting_performances bp ON p.player_id = bp.player_id
            GROUP BY p.player_id, p.full_name
            HAVING AVG(bp.runs_scored) > (SELECT AVG(runs_scored) FROM batting_performances)
            ORDER BY player_avg_runs DESC;
        """,
    },
    10: {
        "title": "Q10: Top scorer per match",
        "description": "The highest individual score in each match (ties included).",
        "sql": """
            SELECT m.match_description, m.match_date, p.full_name AS top_scorer, bp_outer.runs_scored
            FROM batting_performances bp_outer
            JOIN players p ON bp_outer.player_id = p.player_id
            JOIN matches m ON bp_outer.match_id = m.match_id
            WHERE bp_outer.runs_scored = (
                SELECT MAX(bp_inner.runs_scored)
                FROM batting_performances bp_inner
                WHERE bp_inner.match_id = bp_outer.match_id
            )
            ORDER BY m.match_date;
        """,
    },
    11: {
        "title": "Q11: Above-average bowlers",
        "description": "Players whose average wickets per innings exceeds the overall average.",
        "sql": """
            SELECT p.full_name,
                   ROUND(AVG(bp.wickets_taken), 2) AS avg_wickets_per_innings,
                   SUM(bp.wickets_taken) AS total_wickets
            FROM players p
            JOIN bowling_performances bp ON p.player_id = bp.player_id
            GROUP BY p.player_id, p.full_name
            HAVING AVG(bp.wickets_taken) > (SELECT AVG(wickets_taken) FROM bowling_performances)
            ORDER BY avg_wickets_per_innings DESC;
        """,
    },
    12: {
        "title": "Q12: Players who've played all 3 formats",
        "description": "Players with batting performances in Test, ODI, and T20 alike.",
        "sql": """
            SELECT p.full_name, p.country,
                   COUNT(DISTINCT m.match_format) AS formats_played,
                   STRING_AGG(DISTINCT m.match_format, ', ') AS formats_list
            FROM players p
            JOIN batting_performances bp ON p.player_id = bp.player_id
            JOIN matches m ON bp.match_id = m.match_id
            GROUP BY p.player_id, p.full_name, p.country
            HAVING COUNT(DISTINCT m.match_format) = 3
            ORDER BY p.full_name;
        """,
    },
    13: {
        "title": "Q13: Best batting partnerships",
        "description": "Highest combined-run partnerships between consecutive batting positions.",
        "sql": """
            SELECT m.match_description, bp1.innings_number,
                   p1.full_name AS batter_1, bp1.batting_position AS pos_1,
                   p2.full_name AS batter_2, bp2.batting_position AS pos_2,
                   (bp1.runs_scored + bp2.runs_scored) AS partnership_runs
            FROM batting_performances bp1
            JOIN batting_performances bp2
                ON bp1.match_id = bp2.match_id
                AND bp1.innings_number = bp2.innings_number
                AND bp2.batting_position = bp1.batting_position + 1
            JOIN players p1 ON bp1.player_id = p1.player_id
            JOIN players p2 ON bp2.player_id = p2.player_id
            JOIN matches m ON bp1.match_id = m.match_id
            ORDER BY partnership_runs DESC
            LIMIT 10;
        """,
    },
    14: {
        "title": "Q14: Most economical bowlers by venue",
        "description": "Average economy rate for each bowler at each venue they've bowled at.",
        "sql": """
            SELECT p.full_name AS bowler, v.venue_name, v.city,
                   COUNT(bp.match_id) AS matches_bowled_here,
                   ROUND(AVG(bp.economy_rate), 2) AS avg_economy
            FROM bowling_performances bp
            JOIN players p ON bp.player_id = p.player_id
            JOIN matches m ON bp.match_id = m.match_id
            JOIN venues v ON m.venue_id = v.venue_id
            GROUP BY p.player_id, p.full_name, v.venue_id, v.venue_name, v.city
            HAVING COUNT(bp.match_id) >= 1
            ORDER BY avg_economy ASC
            LIMIT 10;
        """,
    },
}


def run_query(question_number: int) -> list[dict]:
    """Executes the SQL for a given question number and returns the results as a list of dicts."""
    query_info = QUERIES.get(question_number)
    if not query_info:
        raise ValueError(f"No query defined for question {question_number}")

    with get_cursor() as cur:
        cur.execute(query_info["sql"])
        return [dict(row) for row in cur.fetchall()]