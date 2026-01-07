"""
Student module (CRUD).
"""
from __future__ import annotations
from typing import Optional
from .utils import get_conn, fetchall, execute

def list_students(class_name: Optional[str]=None) -> list[dict]:
    conn = get_conn()
    sql = """
    SELECT s.roll_no, s.full_name, c.class_name, s.status
    FROM students s
    JOIN classes c ON c.class_id = s.class_id
    """
    params = ()
    if class_name:
        sql += " WHERE c.class_name=?"
        params = (class_name,)
    sql += " ORDER BY s.roll_no"
    rows = fetchall(conn, sql, params)
    conn.close()
    return [dict(r) for r in rows]

def add_student(roll_no: str, full_name: str, class_name: str, status: str="Active") -> None:
    conn = get_conn()
    class_id = conn.execute("SELECT class_id FROM classes WHERE class_name=?", (class_name,)).fetchone()
    if not class_id:
        raise ValueError(f"Unknown class_name: {class_name}")
    execute(conn, "INSERT INTO students (roll_no, full_name, class_id, status) VALUES (?,?,?,?)",
            (roll_no, full_name, class_id["class_id"], status))
    conn.close()
