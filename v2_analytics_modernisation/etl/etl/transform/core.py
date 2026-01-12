from __future__ import annotations

import pandas as pd
from sqlalchemy import Engine, text

def _clean_strings(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == object:
            df[c] = df[c].astype(str).str.strip()
    return df

def build_dim_date(df_attendance: pd.DataFrame) -> pd.DataFrame:
    """Build dim_date from attendance_date."""
    a = df_attendance.copy()
    a["attendance_date"] = pd.to_datetime(a["attendance_date"], errors="coerce").dt.date
    dates = pd.Series(a["attendance_date"]).dropna().drop_duplicates().sort_values()
    df_date = pd.DataFrame({"date_value": dates})
    dt = pd.to_datetime(df_date["date_value"])
    df_date["date_key"] = dt.dt.strftime("%Y%m%d").astype(int)
    df_date["year"] = dt.dt.year
    df_date["month"] = dt.dt.month
    df_date["month_name"] = dt.dt.strftime("%B")
    df_date["day"] = dt.dt.day
    df_date["week"] = dt.dt.isocalendar().week.astype(int)
    return df_date[["date_key","date_value","year","month","month_name","day","week"]]

def build_dim_student(df_students: pd.DataFrame) -> pd.DataFrame:
    df = _clean_strings(df_students)
    return df[["student_id","roll_no","full_name","class_id","class_name","status"]]

def build_dim_class(df_students: pd.DataFrame) -> pd.DataFrame:
    df = _clean_strings(df_students)
    dim_class = df[["class_id","class_name"]].drop_duplicates(subset=["class_id"]).sort_values("class_id")
    return dim_class

def build_dim_subject(df_subjects: pd.DataFrame) -> pd.DataFrame:
    df = _clean_strings(df_subjects)
    return df[["subject_id","subject_name"]]

def upsert_dim_term(dw: Engine, df_results: pd.DataFrame) -> pd.DataFrame:
    """Insert new term names into dw.dim_term and return mapping term_name -> term_key."""
    terms = sorted(_clean_strings(df_results)["term"].dropna().unique().tolist())
    with dw.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS dw;"))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS dw.dim_term (
              term_key SERIAL PRIMARY KEY,
              term_name TEXT UNIQUE NOT NULL
            );
        """))
        for t in terms:
            conn.execute(text("""
                INSERT INTO dw.dim_term (term_name)
                VALUES (:t)
                ON CONFLICT (term_name) DO NOTHING
            """), {"t": t})

    return pd.read_sql("SELECT term_key, term_name FROM dw.dim_term ORDER BY term_key", dw)

def build_fact_attendance(df_attendance: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build:
      - stg_attendance (cleaned attendance events with date_key)
      - fact_attendance (DW fact schema)
    Business rule:
      Present/Late -> present_flag=1
      Absent/Leave -> 0
    """
    df = _clean_strings(df_attendance)
    df["attendance_date"] = pd.to_datetime(df["attendance_date"], errors="coerce")
    df["status"] = df["status"].astype(str).str.strip().str.title()
    df["date_key"] = df["attendance_date"].dt.strftime("%Y%m%d").astype("Int64")
    df = df.dropna(subset=["date_key","student_id","subject_id"]).copy()
    df["date_key"] = df["date_key"].astype(int)
    df["present_flag"] = df["status"].isin(["Present","Late"]).astype(int)

    stg = df[["attendance_date","date_key","student_id","subject_id","status","present_flag"]].copy()
    fact = df[["date_key","student_id","subject_id","status","present_flag"]].copy()
    return stg, fact

def build_fact_result(df_results: pd.DataFrame, df_term_map: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build:
      - stg_result (cleaned results with term_key)
      - fact_result (DW fact schema with term_key)
    """
    r = _clean_strings(df_results)
    r["term"] = r["term"].astype(str).str.strip()
    r["pass_fail"] = r["pass_fail"].astype(str).str.strip().str.title()

    merged = r.merge(df_term_map, left_on="term", right_on="term_name", how="left")
    if merged["term_key"].isna().any():
        missing = merged.loc[merged["term_key"].isna(), "term"].drop_duplicates().tolist()
        raise ValueError(f"term_key mapping failed for terms: {missing}")

    merged["term_key"] = merged["term_key"].astype(int)

    stg = merged[["student_id","subject_id","term","term_key","obtained_total","max_total","percentage","pass_fail","published"]].copy()
    fact = merged[["student_id","subject_id","term_key","obtained_total","max_total","percentage","pass_fail","published"]].copy()
    return stg, fact
