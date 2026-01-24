# CI Workflows (what each one checks)

These workflows exist to show repeatable quality checks on the main branch.

## run_tests.yml
- Runs unit tests (pytest) for the API service
- Goal: basic correctness and regression protection

## run_dq_checks.yml
- Executes the data-quality rule checks
- Produces DQ summary/report artefacts (JSON/HTML) where configured
- Goal: trust and data validation

## run_etl_smoke.yml
- Runs a lightweight ETL smoke run
- Confirms the pipeline executes end-to-end on sample data
- Goal: “clean machine” reproducibility signal for reviewers
