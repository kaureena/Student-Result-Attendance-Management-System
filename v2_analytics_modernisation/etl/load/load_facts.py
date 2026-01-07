from __future__ import annotations
import sqlite3
import pandas as pd

def _lookup(conn: sqlite3.Connection, table: str, key_col: str, val_col: str, value: str) -> int:
    row = conn.execute(f"SELECT {key_col} FROM {table} WHERE {val_col}=?", (value,)).fetchone()
    if not row:
        raise ValueError(f"Missing dimension value in {table}: {value}")
    return int(row[0])

def load_fact_attendance(conn: sqlite3.Connection, att: pd.DataFrame) -> None:
    conn.execute("""CREATE TABLE IF NOT EXISTS fact_attendance (
      student_key INTEGER, date_key INTEGER, class_key INTEGER, present_flag INTEGER,
      PRIMARY KEY(student_key, date_key, class_key)
    )""")
    for _, r in att.iterrows():
        sk = _lookup(conn, "dim_student", "student_key", "roll_no", r["roll_no"])
        ck = _lookup(conn, "dim_class", "class_key", "class_name", r["class_name"])
        date_key = int(pd.to_datetime(r["attendance_date"]).strftime("%Y%m%d"))
        conn.execute("INSERT OR REPLACE INTO fact_attendance (student_key, date_key, class_key, present_flag) VALUES (?,?,?,?)",
                     (sk, date_key, ck, int(r["present"])))
    conn.commit()

def load_fact_results(conn: sqlite3.Connection, res: pd.DataFrame, pass_threshold: int = 40) -> None:
    conn.execute("""CREATE TABLE IF NOT EXISTS fact_results (
      student_key INTEGER, subject_key INTEGER, date_key INTEGER, class_key INTEGER, term TEXT,
      internal_marks INTEGER, external_marks INTEGER, total_marks INTEGER, pass_fail TEXT,
      PRIMARY KEY(student_key, subject_key, date_key, class_key, term)
    )""")
    for _, r in res.iterrows():
        sk = _lookup(conn, "dim_student", "student_key", "roll_no", r["roll_no"])
        subk = _lookup(conn, "dim_subject", "subject_key", "subject_name", r["subject_name"])
        ck = _lookup(conn, "dim_class", "class_key", "class_name", r["class_name"])
        # Use a fixed 'run date' as date dimension (Term load date) for demo
        date_key = int(pd.Timestamp.today().strftime("%Y%m%d"))
        total = int(r["internal_marks"]) + int(r["external_marks"])
        pass_fail = "Pass" if total >= pass_threshold else "Fail"
        conn.execute("""INSERT OR REPLACE INTO fact_results
        (student_key, subject_key, date_key, class_key, term, internal_marks, external_marks, total_marks, pass_fail)
        VALUES (?,?,?,?,?,?,?,?,?)""",
        (sk, subk, date_key, ck, r["term"], int(r["internal_marks"]), int(r["external_marks"]), total, pass_fail))
    conn.commit()
