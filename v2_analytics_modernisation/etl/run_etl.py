from __future__ import annotations
from pathlib import Path

import pandas as pd

import argparse
from pathlib import Path
from sqlalchemy import create_engine, text

from etl.utils.logger import get_logger
from etl.extract.oltp import extract_from_oltp
from etl.transform.core import (
    build_dim_date,
    build_dim_student,
    build_dim_class,
    build_dim_subject,
    upsert_dim_term,
    build_fact_attendance,
    build_fact_result,
)
from etl.load.dw_ddl import ensure_dw_tables
from etl.load.upsert import upsert_dimensions, upsert_facts


def main() -> None:
    parser = argparse.ArgumentParser(description="OLTP -> DW ETL (PostgreSQL) for Student Attendance & Results")
    parser.add_argument(
        "--oltp-url",
        default="postgresql+psycopg2://postgres:admin123@localhost:5432/Sc_oltp"
    )

    parser.add_argument(
        "--dw-url",
        default="postgresql+psycopg2://postgres:admin123@localhost:5432/sc_dw"
    )
    parser.add_argument("--out-dir", default="data_output", help="Where to write staged CSV exports (optional)")
    # parser.add_argument("--create-views", action="store_true", help="Create curated DW views (dw.v_curated_*)")
    parser.add_argument("--create-views", action="store_true", default=True)
    args = parser.parse_args()

    log_dir = Path("logs/etl")
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "etl_run.log"

    out_dir = Path(args.out_dir)
    staged_dir = out_dir / "staged"
    staged_dir.mkdir(parents=True, exist_ok=True)


    log = get_logger("etl", log_file=log_file)


    oltp = create_engine(args.oltp_url)
    dw = create_engine(args.dw_url)

    # Ensure DW tables exist
    ensure_dw_tables(dw)

    # EXTRACT
    log.info("Extracting from OLTP...")
    data = extract_from_oltp(oltp)

    # TRANSFORM
    log.info("Transforming...")
    dim_student = build_dim_student(data["students"])
    dim_class = build_dim_class(data["students"])
    dim_subject = build_dim_subject(data["subjects"])
    dim_date = build_dim_date(data["attendance"])
    term_map = upsert_dim_term(dw, data["results"])

    stg_attendance, fact_attendance = build_fact_attendance(data["attendance"])
    stg_result, fact_result = build_fact_result(data["results"], term_map)

    # Optional staged exports
    stg_attendance.to_csv(staged_dir / "stg_attendance.csv", index=False)
    stg_result.to_csv(staged_dir / "stg_result.csv", index=False)

    # LOAD (UPSERT)
    log.info("Loading dimensions (UPSERT)...")
    upsert_dimensions(dw, dim_class, dim_student, dim_subject, dim_date)

    log.info("Loading facts (UPSERT)...")
    upsert_facts(dw, stg_attendance, fact_attendance, stg_result, fact_result)

    log.info("ETL done ✅")



    if args.create_views:
        log.info("Creating curated views (dw.v_curated_*) ...")
        sql_path = Path(__file__).resolve().parent / "sql" / "curated_views.sql"
        with dw.begin() as conn:
            conn.execute(text(sql_path.read_text(encoding="utf-8")))
        log.info("Curated views ready ✅")

        curated_dir = Path("data_output/curated")
        curated_dir.mkdir(parents=True, exist_ok=True)

        log.info("Exporting curated files...")

        pd.read_sql(
            "SELECT * FROM dw.v_curated_attendance_monthly",
            dw
        ).to_csv(curated_dir / "attendance_monthly.csv", index=False)

        pd.read_sql(
            "SELECT * FROM dw.v_curated_results_term",
            dw
        ).to_csv(curated_dir / "results_term.csv", index=False)

        log.info("Curated files saved to %s", curated_dir)


if __name__ == "__main__":
    main()
