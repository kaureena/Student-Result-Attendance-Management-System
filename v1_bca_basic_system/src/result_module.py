"""
Results module.
"""
from __future__ import annotations
from .utils import get_conn, fetchall, execute

PASS_THRESHOLD = 40

def upsert_marks(roll_no: str, subject_name: str, term: str, internal_marks: int, external_marks: int) -> None:
    conn = get_conn()
    s = conn.execute("SELECT student_id FROM students WHERE roll_no=?", (roll_no,)).fetchone()
    if not s:
        conn.close()
        raise ValueError(f"Unknown roll number: {roll_no}")
    sub = conn.execute("SELECT subject_id FROM subjects WHERE subject_name=?", (subject_name,)).fetchone()
    if not sub:
        conn.close()
        raise ValueError(f"Unknown subject: {subject_name}")

    total = internal_marks + external_marks
    pass_fail = "Pass" if total >= PASS_THRESHOLD else "Fail"
    execute(conn, """
    INSERT OR REPLACE INTO results (student_id, subject_id, term, internal_marks, external_marks, total_marks, pass_fail)
    VALUES (?,?,?,?,?,?,?)
    """, (s["student_id"], sub["subject_id"], term, internal_marks, external_marks, total, pass_fail))
    conn.close()

def list_results(class_name: str, subject_name: str, term: str="Term-1") -> list[dict]:
    conn = get_conn()
    sql = """
    SELECT s.roll_no, s.full_name, r.internal_marks, r.external_marks, r.total_marks, r.pass_fail
    FROM students s
    JOIN classes c ON c.class_id=s.class_id
    JOIN results r ON r.student_id=s.student_id
    JOIN subjects sub ON sub.subject_id=r.subject_id
    WHERE c.class_name=? AND sub.subject_name=? AND r.term=?
    ORDER BY s.roll_no
    """
    rows = fetchall(conn, sql, (class_name, subject_name, term))
    conn.close()
    return [dict(r) for r in rows]
