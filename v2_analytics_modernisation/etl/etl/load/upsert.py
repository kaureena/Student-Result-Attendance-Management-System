from __future__ import annotations

import pandas as pd
from sqlalchemy import Engine, text

def _stage(df: pd.DataFrame, dw: Engine, table: str) -> None:
    df.to_sql(table, dw, schema="dw", if_exists="replace", index=False)

def upsert_dimensions(dw: Engine,
                      dim_class: pd.DataFrame,
                      dim_student: pd.DataFrame,
                      dim_subject: pd.DataFrame,
                      dim_date: pd.DataFrame) -> None:
    _stage(dim_class, dw, "stg_dim_class")
    _stage(dim_student, dw, "stg_dim_student")
    _stage(dim_subject, dw, "stg_dim_subject")
    _stage(dim_date, dw, "stg_dim_date")

    with dw.begin() as conn:
        conn.execute(text("""
            INSERT INTO dw.dim_class (class_id, class_name)
            SELECT class_id, class_name
            FROM dw.stg_dim_class
            ON CONFLICT (class_id) DO UPDATE
            SET class_name = EXCLUDED.class_name;
        """))

        conn.execute(text("""
            INSERT INTO dw.dim_student (student_id, roll_no, full_name, class_id, class_name, status)
            SELECT student_id, roll_no, full_name, class_id, class_name, status
            FROM dw.stg_dim_student
            ON CONFLICT (student_id) DO UPDATE
            SET roll_no    = EXCLUDED.roll_no,
                full_name  = EXCLUDED.full_name,
                class_id   = EXCLUDED.class_id,
                class_name = EXCLUDED.class_name,
                status     = EXCLUDED.status;
        """))

        conn.execute(text("""
            INSERT INTO dw.dim_subject (subject_id, subject_name)
            SELECT subject_id, subject_name
            FROM dw.stg_dim_subject
            ON CONFLICT (subject_id) DO UPDATE
            SET subject_name = EXCLUDED.subject_name;
        """))

        conn.execute(text("""
            INSERT INTO dw.dim_date (date_key, date_value, year, month, month_name, day, week)
            SELECT date_key, date_value, year, month, month_name, day, week
            FROM dw.stg_dim_date
            ON CONFLICT (date_key) DO UPDATE
            SET date_value = EXCLUDED.date_value,
                year       = EXCLUDED.year,
                month      = EXCLUDED.month,
                month_name = EXCLUDED.month_name,
                day        = EXCLUDED.day,
                week       = EXCLUDED.week;
        """))

def upsert_facts(dw: Engine,
                 stg_attendance: pd.DataFrame,
                 fact_attendance: pd.DataFrame,
                 stg_result: pd.DataFrame,
                 fact_result: pd.DataFrame) -> None:
    _stage(stg_attendance, dw, "stg_attendance")
    _stage(stg_result, dw, "stg_result")
    _stage(fact_attendance, dw, "stg_fact_attendance")
    _stage(fact_result, dw, "stg_fact_result")

    with dw.begin() as conn:
        conn.execute(text("""
            INSERT INTO dw.fact_attendance (date_key, student_id, subject_id, status, present_flag)
            SELECT date_key, student_id, subject_id, status, present_flag
            FROM dw.stg_fact_attendance
            ON CONFLICT (date_key, student_id, subject_id) DO UPDATE
            SET status = EXCLUDED.status,
                present_flag = EXCLUDED.present_flag;
        """))

        conn.execute(text("""
            INSERT INTO dw.fact_result (student_id, subject_id, term_key, obtained_total, max_total, percentage, pass_fail, published)
            SELECT student_id, subject_id, term_key, obtained_total, max_total, percentage, pass_fail, published
            FROM dw.stg_fact_result
            ON CONFLICT (student_id, subject_id, term_key) DO UPDATE
            SET obtained_total = EXCLUDED.obtained_total,
                max_total      = EXCLUDED.max_total,
                percentage     = EXCLUDED.percentage,
                pass_fail      = EXCLUDED.pass_fail,
                published      = EXCLUDED.published;
        """))

