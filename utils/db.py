import os
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path

_DB_URL = os.getenv("DATABASE_URL")

def get_conn():
    url = _DB_URL
    if not url:
        raise RuntimeError("DATABASE_URL environment variable is not set.")
    # Neon-friendly: enforce SSL
    return psycopg2.connect(url, cursor_factory=RealDictCursor, sslmode="require")

def query(sql, params=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            if cur.description:
                return cur.fetchall()
            return []

def execute(sql, params=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            conn.commit()

def _split_sql(sql_text: str):
    parts = []
    stmt = []
    in_s = None
    escape = False
    for ch in sql_text:
        if in_s:
            stmt.append(ch)
            if ch == in_s and not escape:
                in_s = None
            escape = (ch == '"' and not escape)
        else:
            if ch in ("'", '"'):
                in_s = ch
                stmt.append(ch)
            elif ch == ";":
                s = "".join(stmt).strip()
                if s:
                    parts.append(s)
                stmt = []
            else:
                stmt.append(ch)
    tail = "".join(stmt).strip()
    if tail:
        parts.append(tail)
    return parts

def run_sql_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        sql_text = f.read()
    statements = _split_sql(sql_text)
    with get_conn() as conn:
        with conn.cursor() as cur:
            for s in statements:
                cur.execute(s)
        conn.commit()

# --- Helpers for Setup Wizard / Auto-init ---

def table_exists(name: str) -> bool:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT EXISTS (
                  SELECT 1 FROM information_schema.tables
                  WHERE table_schema='public' AND table_name=%s
                ) AS ok
            """, (name,))
            row = cur.fetchone()
            return bool(row["ok"]) if row else False

def users_count() -> int:
    if not table_exists("users"):
        return 0
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) AS c FROM users")
            row = cur.fetchone()
            return int(row["c"]) if row else 0

def ensure_schema():
    """Idempotently create schema and optional seeds if missing."""
    if not table_exists("users"):
        if Path("sql/init_db.sql").exists():
            run_sql_file("sql/init_db.sql")
        if Path("sql/seed_calendar.sql").exists():
            run_sql_file("sql/seed_calendar.sql")

def needs_setup() -> bool:
    """True if DATABASE_URL missing or schema/users not ready."""
    if not _DB_URL:
        return True
    try:
        return users_count() == 0
    except Exception:
        return True
