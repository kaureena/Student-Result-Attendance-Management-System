from __future__ import annotations
from fastapi import APIRouter
from ..services.db import get_conn

router = APIRouter()

@router.get("/")
def results_by_subject(class_name: str, subject_name: str, term: str = "Term-1"):
    conn = get_conn()
    sql = """
    SELECT s.roll_no, s.full_name, r.internal_marks, r.external_marks, r.total_marks, r.pass_fail
    FROM results r
    JOIN students s ON s.student_id=r.student_id
    JOIN classes c ON c.class_id=s.class_id
    JOIN subjects sub ON sub.subject_id=r.subject_id
    WHERE c.class_name=? AND sub.subject_name=? AND r.term=?
    ORDER BY s.roll_no
    """
    rows = [dict(r) for r in conn.execute(sql, (class_name, subject_name, term)).fetchall()]
    conn.close()
    return rows
