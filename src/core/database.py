import logging
from contextlib import contextmanager
from typing import Generator
import psycopg2
from psycopg2.extensions import connection
from src.core.config import settings

logger = logging.getLogger(__name__)


def _get_connection_string() -> str:
    if settings.DIRECT_URL:
        return settings.DIRECT_URL
    if settings.DATABASE_URL:
        return settings.DATABASE_URL.split("?")[0]
    return ""


@contextmanager
def get_db_connection() -> Generator[connection, None, None]:
    conn_str = _get_connection_string()
    if not conn_str:
        raise ConnectionError("Chưa cấu hình DATABASE_URL hoặc DIRECT_URL trong .env")
    conn = psycopg2.connect(conn_str, connect_timeout=10)
    try:
        yield conn
    finally:
        conn.close()
