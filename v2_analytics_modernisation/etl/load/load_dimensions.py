from __future__ import annotations
import sqlite3
import pandas as pd

def upsert_dim_student(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    conn.execute("CREATE TABLE IF NOT EXISTS dim_student (student_key INTEGER PRIMARY KEY AUTOINCREMENT, roll_no TEXT UNIQUE, student_name TEXT)")
    for _, r in df.iterrows():
        conn.execute("INSERT OR IGNORE INTO dim_student (roll_no, student_name) VALUES (?,?)", (r["roll_no"], r["student_name"]))
    conn.commit()

def upsert_dim_subject(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    conn.execute("CREATE TABLE IF NOT EXISTS dim_subject (subject_key INTEGER PRIMARY KEY AUTOINCREMENT, subject_name TEXT UNIQUE, max_marks INTEGER)")
    for _, r in df.iterrows():
        conn.execute("INSERT OR IGNORE INTO dim_subject (subject_name, max_marks) VALUES (?,?)", (r["subject_name"], int(r["max_marks"])))
    conn.commit()

def upsert_dim_class(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    conn.execute("CREATE TABLE IF NOT EXISTS dim_class (class_key INTEGER PRIMARY KEY AUTOINCREMENT, class_name TEXT UNIQUE)")
    for _, r in df.iterrows():
        conn.execute("INSERT OR IGNORE INTO dim_class (class_name) VALUES (?)", (r["class_name"],))
    conn.commit()

def upsert_dim_date(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    conn.execute("CREATE TABLE IF NOT EXISTS dim_date (date_key INTEGER PRIMARY KEY, full_date TEXT, month INTEGER, year INTEGER)")
    for _, r in df.iterrows():
        conn.execute("INSERT OR IGNORE INTO dim_date (date_key, full_date, month, year) VALUES (?,?,?,?)",
                     (int(r["date_key"]), r["full_date"], int(r["month"]), int(r["year"])))
    conn.commit()
