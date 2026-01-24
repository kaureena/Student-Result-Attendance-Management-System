# v0.1.0 — Baseline + Modernisation scaffold

## What this release contains
- v1 (BCA baseline): Student/Attendance/Results modules + sample exports + UI screenshots
- v2 (modernisation): ETL pipeline + data quality checks + warehouse SQL + Power BI artefacts + docs
- Documentation: architecture, data model notes, ETL design, DQ rule catalogue, screenshots/diagrams
- CI: workflows for tests, DQ checks, and ETL smoke runs

## Quick start (local)

v1 baseline:
```bash
cd v1_bca_basic_system
python -m pip install -r requirements.txt
python src/main.py
```

v2 ETL + DQ demo:
```bash
cd v2_analytics_modernisation
python -m pip install -r requirements.txt
python etl/run_etl.py
python dq_data_quality/run_checks.py
```

## Notes
- Data in this repo is synthetic/sample only (no real student data).
