# Student Attendance & Results ETL (PostgreSQL)

A clean **OLTP -> DW -> BI** pipeline with **UPSERT** loads and **Power BI-friendly keys** (uses `term_key`).

## Install
```bash
pip install pandas sqlalchemy psycopg2-binary
```

## 1) Create OLTP view
Run `sql/oltp_views.sql` in your OLTP database (public schema) to create:
- `public.v_result_summary`

## 2) Run ETL
```bash
python run_etl.py   --oltp-url "postgresql+psycopg2://USER:PASSWORD@HOST:5432/OLTP_DB"   --dw-url   "postgresql+psycopg2://USER:PASSWORD@HOST:5432/DW_DB"   --out-dir  "data_output"   --create-views
```

## 3) Use in Power BI
Connect to DW database and use these views:
- `dw.v_curated_attendance_monthly`
- `dw.v_curated_results_term`

Recommended relationships:
- fact_attendance.date_key -> dim_date.date_key
- fact_attendance.student_id -> dim_student.student_id
- fact_attendance.subject_id -> dim_subject.subject_id
- fact_result.term_key -> dim_term.term_key
- fact_result.student_id -> dim_student.student_id
- fact_result.subject_id -> dim_subject.subject_id
