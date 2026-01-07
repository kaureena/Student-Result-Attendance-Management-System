"""
Utilities for v1 baseline app.
"""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Iterable, Any, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "database" / "local.db"

def get_conn(db_path: Optional[Path]=None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def fetchall(conn: sqlite3.Connection, sql: str, params: Tuple[Any, ...]=()) -> list[sqlite3.Row]:
    cur = conn.execute(sql, params)
    return cur.fetchall()

def execute(conn: sqlite3.Connection, sql: str, params: Tuple[Any, ...]=()) -> None:
    conn.execute(sql, params)
    conn.commit()
