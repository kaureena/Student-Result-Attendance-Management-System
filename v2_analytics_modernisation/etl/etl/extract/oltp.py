from __future__ import annotations
import pandas as pd
from sqlalchemy import Engine

def extract_from_oltp(oltp: Engine) -> dict[str, pd.DataFrame]:
    """
    Extract raw datasets from OLTP (public schema) in PostgreSQL.
    Returns DataFrames:
      - students (joined with classes)
      - subjects
      - attendance
      - results (from view public.v_result_summary)
    """
    df_students = pd.read_sql(
        """
        SELECT
          s.student_id,
          s.roll_no,
          s.full_name,
          s.class_id,
          c.class_name,
          s.status
        FROM public.students s
        JOIN public.classes c ON c.class_id = s.class_id
        """,
        oltp,
    )

    df_subjects = pd.read_sql(
        """
        SELECT subject_id, subject_name
        FROM public.subjects
        """,
        oltp,
    )

    df_attendance = pd.read_sql(
        """
        SELECT student_id, subject_id, attendance_date, status
        FROM public.attendance
        """,
        oltp,
    )

    # Term-wise totals (obtained_total/max_total/percentage/pass_fail)
    df_results = pd.read_sql(
        """
        SELECT student_id, subject_id, term, obtained_total, max_total, percentage, pass_fail, published
        FROM public.v_result_summary
        """,
        oltp,
    )

    return {
        "students": df_students,
        "subjects": df_subjects,
        "attendance": df_attendance,
        "results": df_results,
    }
