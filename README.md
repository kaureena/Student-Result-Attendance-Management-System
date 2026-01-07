# Student Result & Attendance Management System (v1 + v2 Modernised)

This repository contains **two connected versions** of the same project:

- **v1 (BCA baseline):** a simple student administration system (students, attendance, marks, exports).
- **v2 (Data Analytics modernisation):** the same dataset modernised into a reporting platform (ETL, warehouse, data quality, Power BI + SharePoint embedding plan).

> **Note:** This is a portfolio repository using **synthetic / anonymised** sample data.

## Repository layout (high level)
- `v1_bca_basic_system/` — baseline application and local SQLite demo DB
- `v2_analytics_modernisation/` — ETL + warehouse + DQ + API + Docker templates
- `docs/` — documentation, Mermaid diagrams, and evidence-style logs
- `logs/sample_logs_only/` — sample run logs (ETL/DQ/API)

## Quick start (v1)
```bash
cd v1_bca_basic_system
python -m pip install -r requirements.txt
python src/main.py
```

## Quick start (v2 ETL demo)
```bash
cd v2_analytics_modernisation
python -m pip install -r requirements.txt
python etl/run_etl.py --source sqlite --generate-samples
python dq_data_quality/run_checks.py
```

## Important limitations (known)
- **Power BI `.pbix`** cannot be generated programmatically here. A placeholder file is provided; replace it with your real PBIX when ready.
- **Parquet outputs** are not included because Parquet writer libraries are not bundled in this environment. This template uses CSV for staged/curated outputs by default (you can switch to Parquet later by installing `pyarrow`).

