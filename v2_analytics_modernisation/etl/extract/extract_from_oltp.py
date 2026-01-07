from __future__ import annotations
import sqlite3
from pathlib import Path
import pandas as pd

def extract_from_sqlite(sqlite_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    conn = sqlite3.connect(sqlite_path)
    attendance = pd.read_sql_query("""
        SELECT s.roll_no, a.attendance_date, a.present, c.class_name
        FROM attendance a
        JOIN students s ON s.student_id=a.student_id
        JOIN classes c ON c.class_id=s.class_id
    """, conn)
    results = pd.read_sql_query("""
        SELECT s.roll_no, sub.subject_name, r.term, r.internal_marks, r.external_marks, c.class_name
        FROM results r
        JOIN students s ON s.student_id=r.student_id
        JOIN subjects sub ON sub.subject_id=r.subject_id
        JOIN classes c ON c.class_id=s.class_id
    """, conn)
    conn.close()
    return attendance, results
