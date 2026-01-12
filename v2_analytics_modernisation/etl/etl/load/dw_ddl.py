from __future__ import annotations
from sqlalchemy import Engine, text

def ensure_dw_tables(dw: Engine) -> None:
    """Create DW schema and tables if not exist (idempotent)."""
    with dw.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS dw;"))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS dw.dim_class (
          class_id INT PRIMARY KEY,
          class_name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dw.dim_student (
          student_id INT PRIMARY KEY,
          roll_no TEXT,
          full_name TEXT,
          class_id INT REFERENCES dw.dim_class(class_id),
          class_name TEXT,
          status TEXT
        );

        CREATE TABLE IF NOT EXISTS dw.dim_subject (
          subject_id INT PRIMARY KEY,
          subject_name TEXT
        );

        CREATE TABLE IF NOT EXISTS dw.dim_date (
          date_key INT PRIMARY KEY,
          date_value DATE UNIQUE NOT NULL,
          year INT,
          month INT,
          month_name TEXT,
          day INT,
          week INT
        );

        CREATE TABLE IF NOT EXISTS dw.dim_term (
          term_key SERIAL PRIMARY KEY,
          term_name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dw.fact_attendance (
          date_key INT REFERENCES dw.dim_date(date_key),
          student_id INT REFERENCES dw.dim_student(student_id),
          subject_id INT REFERENCES dw.dim_subject(subject_id),
          status TEXT,
          present_flag INT,
          PRIMARY KEY (date_key, student_id, subject_id)
        );

        CREATE TABLE IF NOT EXISTS dw.fact_result (
          student_id INT REFERENCES dw.dim_student(student_id),
          subject_id INT REFERENCES dw.dim_subject(subject_id),
          term_key INT REFERENCES dw.dim_term(term_key),
          obtained_total INT,
          max_total INT,
          percentage NUMERIC(6,2),
          pass_fail TEXT,
          published BOOLEAN,
          PRIMARY KEY (student_id, subject_id, term_key)
        );
        """))
