# v2 — Analytics Modernisation

This layer modernises the v1 dataset into a BI-friendly reporting platform.

## Components
- `oltp_database/` — operational schema (reference)
- `etl/` — extract/transform/load into star schema outputs
- `warehouse/` — star schema DDL
- `dq_data_quality/` — validation rules + reports
- `bi_powerbi/` — dashboard plan (PBIX placeholder)
- `api_service/` — optional FastAPI service
- `docker/` — Docker templates for local running

## Run ETL (demo)
```bash
python -m pip install -r requirements.txt
python etl/run_etl.py --generate-samples
python dq_data_quality/run_checks.py
```
