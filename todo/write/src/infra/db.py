import os
from contextlib import contextmanager
from typing import Generator
import psycopg
from psycopg.rows import dict_row

def get_db_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return url

@contextmanager
def get_db_connection() -> Generator[psycopg.Connection, None, None]:
    url = get_db_url()
    with psycopg.connect(url, row_factory=dict_row) as conn:
        yield conn

@contextmanager
def get_db_transaction() -> Generator[psycopg.Cursor, None, None]:
    with get_db_connection() as conn:
        with conn.transaction():
            with conn.cursor() as cur:
                yield cur
