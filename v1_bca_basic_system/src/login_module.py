"""
Login module (simple baseline).
"""
from __future__ import annotations
from typing import Optional
from .utils import get_conn

def authenticate(username: str, password: str) -> bool:
    conn = get_conn()
    row = conn.execute(
        "SELECT 1 FROM users WHERE username=? AND password=?",
        (username.strip(), password.strip()),
    ).fetchone()
    conn.close()
    return row is not None
