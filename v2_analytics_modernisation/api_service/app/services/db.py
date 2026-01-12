from __future__ import annotations
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OLTP_DB = ROOT / "v1_bca_basic_system" / "database" / "local.db"

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(OLTP_DB)
    conn.row_factory = sqlite3.Row
    return conn
