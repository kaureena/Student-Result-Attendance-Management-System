# Environment (Dual-Env)

This repo has two run profiles.

## Recommended runtime
- Python **3.11** (or 3.12)
- Use a virtual environment

## v1 profile — Baseline app (SQLite demo)
From repo root:

```bash
cd v1_bca_basic_system
python -m pip install -r requirements.txt
python src/main.py
```

## v2 profile — ETL + Data Quality demo
From repo root:

```bash
cd v2_analytics_modernisation
python -m pip install -r requirements.txt
python etl/run_etl.py
python dq_data_quality/run_checks.py
```

Notes:
- If your README uses CLI flags like `--source sqlite --generate-samples`,
  make sure the scripts support those flags, OR update the README to the real command.

## Secrets / configuration
- Do not commit secrets.
- Use environment variables (see `.env.example`).
- Document any required keys in this file (add a small table here if needed).

## Transparency note (publication vs original academic period)
This repository was published and curated as a portfolio artefact in **Jan 2026**.
Git commit dates reflect publication/packaging, not necessarily the original academic calendar.
