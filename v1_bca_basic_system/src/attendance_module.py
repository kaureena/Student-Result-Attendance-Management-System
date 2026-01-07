"""
Attendance module.
"""
from __future__ import annotations
from datetime import date
from .utils import get_conn, fetchall, execute

def mark_attendance(attendance_date: str, roll_no: str, present: bool) -> None:
    conn = get_conn()
    row = conn.execute("SELECT student_id FROM students WHERE roll_no=?", (roll_no,)).fetchone()
    if not row:
        conn.close()
        raise ValueError(f"Unknown roll number: {roll_no}")
    student_id = row["student_id"]
    execute(conn,
        "INSERT OR REPLACE INTO attendance (student_id, attendance_date, present) VALUES (?,?,?)",
        (student_id, attendance_date, 1 if present else 0)
    )
    conn.close()

def list_attendance(attendance_date: str, class_name: str) -> list[dict]:
    conn = get_conn()
    sql = """
    SELECT s.roll_no, s.full_name, a.attendance_date, a.present
    FROM students s
    JOIN classes c ON c.class_id=s.class_id
    LEFT JOIN attendance a ON a.student_id=s.student_id AND a.attendance_date=?
    WHERE c.class_name=?
    ORDER BY s.roll_no
    """
    rows = fetchall(conn, sql, (attendance_date, class_name))
    conn.close()
    out = []
    for r in rows:
        out.append({
            "roll_no": r["roll_no"],
            "full_name": r["full_name"],
            "attendance_date": r["attendance_date"] or attendance_date,
            "present": "Yes" if (r["present"] == 1) else "No",
        })
    return out
