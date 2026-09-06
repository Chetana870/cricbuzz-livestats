"""
Centralized database connection handler.

Every other module (services, CRUD, analytics) imports get_connection()
from here instead of calling psycopg2 directly. This is the single
choke point for database access, per the project's architecture design.
"""

import psycopg2
import psycopg2.extras
from contextlib import contextmanager
import logging

from config import DB_CONFIG

logger = logging.getLogger(__name__)


def get_connection():
    """
    Create and return a new psycopg2 connection using settings from config.py.
    Raises psycopg2.OperationalError if the connection fails (e.g. wrong
    credentials, database not running) — callers should handle this.
    """
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            dbname=DB_CONFIG["dbname"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Database connection failed: {e}")
        raise


@contextmanager
def get_cursor(commit: bool = False):
    """
    Context manager that yields a dict-cursor and handles commit/rollback
    and connection cleanup automatically.

    Usage:
        with get_cursor(commit=True) as cur:
            cur.execute("INSERT INTO teams (team_name, country) VALUES (%s, %s)", (name, country))
    """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        yield cur
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
