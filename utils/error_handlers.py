"""
Reusable error-handling helpers.

safe_db_call wraps a database operation and returns (result, error_message)
instead of letting raw exceptions (IntegrityError, OperationalError, etc.)
bubble up to Streamlit as an unstyled traceback.
"""

import logging
import psycopg2

logger = logging.getLogger(__name__)


def safe_db_call(func, *args, **kwargs):
    """
    Runs func(*args, **kwargs) and returns (result, error_message).
    On success: (result, None)
    On failure: (None, "a friendly error string")

    Usage:
        result, error = safe_db_call(create_team, name, country)
        if error:
            st.error(error)
        else:
            st.success(f"Created: {result}")
    """
    try:
        result = func(*args, **kwargs)
        return result, None

    except psycopg2.errors.UniqueViolation:
        logger.warning(f"Unique constraint violated calling {func.__name__}")
        return None, "That name already exists — please use a different one."

    except psycopg2.errors.ForeignKeyViolation:
        logger.warning(f"Foreign key violation calling {func.__name__}")
        return None, "This record is still referenced elsewhere and can't be deleted or changed that way."

    except psycopg2.OperationalError as e:
        logger.error(f"Database connection error in {func.__name__}: {e}")
        return None, "Could not connect to the database. Please check it's running and try again."

    except Exception as e:
        logger.error(f"Unexpected error in {func.__name__}: {e}")
        return None, f"Something unexpected went wrong: {e}"