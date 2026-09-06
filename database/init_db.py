"""
Run this once to create all tables and load sample seed data:

    python database/init_db.py

Safe to re-run against a fresh database only — it does not drop existing
tables. If you need a clean slate, drop the database and recreate it first.
"""

import logging
from database.db_connection import get_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_sql_file(conn, filepath: str):
    with open(filepath, "r") as f:
        sql = f.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()
    logger.info(f"Executed {filepath}")


def main():
    conn = get_connection()
    try:
        run_sql_file(conn, "sql/schema.sql")
        run_sql_file(conn, "sql/seed_data.sql")
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
