#!/usr/bin/env bash
set -euo pipefail

echo "Starting v2 ETL demo..."
python etl/run_etl.py --source sqlite
python dq_data_quality/run_checks.py
echo "Done."
