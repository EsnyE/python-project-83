import os
import psycopg2
from psycopg2.extras import DictCursor
from urllib.parse import urlparse
from datetime import datetime
import validators


def get_db_connection():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return psycopg2.connect(database_url)


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}".lower()


def validate_url(url):
    if not url:
        return False,
    if len(url) > 255:
        return False,
    if not validators.url(url):
        return False,
    return True, None


def add_url(url):
    normalized = normalize_url(url)
    
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                (normalized, datetime.now())
            )
            url_id = cur.fetchone()['id']
            conn.commit()
            return url_id


def get_url_by_name(name):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE name = %s", (name,))
            return cur.fetchone()


def get_url_by_id(url_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
            return cur.fetchone()


def get_all_urls():
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls ORDER BY created_at DESC")
            return cur.fetchall()


def add_url_check(url_id, status_code, h1, title, description):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                """INSERT INTO url_checks 
                   (url_id, status_code, h1, title, description, created_at) 
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (url_id, status_code, h1, title, description, datetime.now())
            )
            conn.commit()


def get_url_checks(url_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                "SELECT * FROM url_checks WHERE url_id = %s ORDER BY created_at DESC",
                (url_id,)
            )
            return cur.fetchall()


def get_last_check(url_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                """SELECT * FROM url_checks 
                   WHERE url_id = %s 
                   ORDER BY created_at DESC 
                   LIMIT 1""",
                (url_id,)
            )
            return cur.fetchone()

def add_url_check(url_id, status_code=None, h1=None, title=None, description=None):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                """INSERT INTO url_checks 
                   (url_id, status_code, h1, title, description, created_at) 
                   VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
                (url_id, status_code, h1, title, description, datetime.now())
            )
            check_id = cur.fetchone()['id']
            conn.commit()
            return check_id


def get_url_checks(url_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                "SELECT * FROM url_checks WHERE url_id = %s ORDER BY created_at DESC",
                (url_id,)
            )
            return cur.fetchall()


def get_last_check(url_id):
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                """SELECT * FROM url_checks 
                   WHERE url_id = %s 
                   ORDER BY created_at DESC 
                   LIMIT 1""",
                (url_id,)
            )
            return cur.fetchone()