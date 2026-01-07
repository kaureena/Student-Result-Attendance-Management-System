from __future__ import annotations
from fastapi import APIRouter
from ..services.db import get_conn

router = APIRouter()

@router.get("/")
def list_students(class_name: str | None = None):
    conn = get_conn()
    sql = """
    SELECT s.roll_no, s.full_name, c.class_name, s.status
    FROM students s JOIN classes c ON c.class_id=s.class_id
    """
    params = []
    if class_name:
        sql += " WHERE c.class_name=?"
        params.append(class_name)
    sql += " ORDER BY s.roll_no"
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows
