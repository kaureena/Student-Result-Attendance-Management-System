from __future__ import annotations
from fastapi import APIRouter
from ..services.db import get_conn

router = APIRouter()

@router.get("/")
def attendance_by_date(attendance_date: str, class_name: str):
    conn = get_conn()
    sql = """
    SELECT s.roll_no, s.full_name, a.attendance_date, a.present, c.class_name
    FROM students s
    JOIN classes c ON c.class_id=s.class_id
    LEFT JOIN attendance a ON a.student_id=s.student_id AND a.attendance_date=?
    WHERE c.class_name=?
    ORDER BY s.roll_no
    """
    rows = []
    for r in conn.execute(sql, (attendance_date, class_name)).fetchall():
        rows.append({
            "roll_no": r["roll_no"],
            "full_name": r["full_name"],
            "attendance_date": r["attendance_date"] or attendance_date,
            "present": bool(r["present"]) if r["present"] is not None else None,
            "class_name": r["class_name"],
        })
    conn.close()
    return rows
