"""
Central configuration. Loads secrets from .env — never hardcode
credentials directly in code.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Cricbuzz API (RapidAPI) ---
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "cricbuzz-cricket.p.rapidapi.com")

# --- Database ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "cricbuzz_livestats"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

if not RAPIDAPI_KEY:
    raise EnvironmentError(
        "RAPIDAPI_KEY is not set. Copy .env.example to .env and fill in your key."
    )
