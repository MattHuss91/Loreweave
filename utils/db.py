import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_conn():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL environment variable is not set.")
    return psycopg2.connect(url, cursor_factory=RealDictCursor)

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
            escape = (ch == "\" and not escape)
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
