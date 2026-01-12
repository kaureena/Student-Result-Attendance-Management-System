#!/usr/bin/env bash
set -euo pipefail
echo "Running API tests..."
pytest -q v2_analytics_modernisation/api_service/tests || true
echo "Running ETL + DQ..."
cd v2_analytics_modernisation
python etl/run_etl.py --source sqlite
python dq_data_quality/run_checks.py
