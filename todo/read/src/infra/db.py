import os
from contextlib import contextmanager
from typing import Generator
import psycopg
from psycopg.rows import dict_row

def get_db_url() -> str:
    # Favor READ_DATABASE_URL if present (e.g. for RDS Reader endpoint)
    url = os.environ.get("READ_DATABASE_URL") or os.environ.get("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return url

@contextmanager
def get_db_connection(autocommit: bool = False) -> Generator[psycopg.Connection, None, None]:
    url = get_db_url()
    with psycopg.connect(url, row_factory=dict_row, autocommit=autocommit) as conn:
        yield conn

@contextmanager
def get_db_cursor() -> Generator[psycopg.Cursor, None, None]:
    """
    Get a cursor with autocommit=True. Useful for read-only queries 
    where explicit transaction management is not needed.
    """
    with get_db_connection(autocommit=True) as conn:
        with conn.cursor() as cur:
            yield cur

@contextmanager
def get_db_transaction() -> Generator[psycopg.Cursor, None, None]:
    """
    Get a cursor within a transaction. Required for projections 
    to ensure atomic updates of read model and event tracking.
    """
    with get_db_connection() as conn:
        with conn.transaction():
            with conn.cursor() as cur:
                yield cur
