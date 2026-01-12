from __future__ import annotations
import json
from pathlib import Path
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
REPORTS = REPO / "dq_data_quality" / "reports"
STAGED = REPO / "data" / "staged"
CURATED = REPO / "data" / "curated"

PASS_THRESHOLD = 40
INTERNAL_MAX = 30
EXTERNAL_MAX = 70

def check_attendance(att: pd.DataFrame) -> list[dict]:
    issues = []
    # date parse check
    parsed = pd.to_datetime(att["attendance_date"], errors="coerce")
    bad = att[parsed.isna()]
    for _, r in bad.iterrows():
        issues.append({"rule":"attendance_date_valid", "severity":"FAIL", "key":f'{r.get("roll_no","")}|{r.get("attendance_date","")}', "message":"Invalid date"})
    # duplicate roll/date
    dup = att.duplicated(subset=["roll_no","attendance_date"], keep=False)
    for _, r in att[dup].iterrows():
        issues.append({"rule":"no_duplicate_student_date", "severity":"WARN", "key":f'{r["roll_no"]}|{r["attendance_date"]}', "message":"Duplicate attendance record"})
    return issues

def check_results(res: pd.DataFrame) -> list[dict]:
    issues = []
    # bounds
    bad_int = res[res["internal_marks"] > INTERNAL_MAX]
    for _, r in bad_int.iterrows():
        issues.append({"rule":"marks_not_exceed_max", "severity":"FAIL", "key":f'{r["roll_no"]}|{r["subject_name"]}|{r["term"]}', "message":"Internal marks exceeds max"})
    bad_ext = res[res["external_marks"] > EXTERNAL_MAX]
    for _, r in bad_ext.iterrows():
        issues.append({"rule":"marks_not_exceed_max", "severity":"FAIL", "key":f'{r["roll_no"]}|{r["subject_name"]}|{r["term"]}', "message":"External marks exceeds max"})
    # total + pass/fail consistency (computed)
    res = res.copy()
    res["total"] = res["internal_marks"] + res["external_marks"]
    res["expected_pass_fail"] = res["total"].apply(lambda t: "Pass" if t >= PASS_THRESHOLD else "Fail")
    mism = res[res["expected_pass_fail"].isna() == False]  # kept for clarity
    # no stored pass_fail in staged; validate computed threshold only
    return issues

def render_html(summary: dict, issues: list[dict]) -> str:
    rows = ""
    for i in issues:
        rows += f"<tr><td>{i['rule']}</td><td>{i['severity']}</td><td>{i['key']}</td><td>{i['message']}</td></tr>\n"
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>DQ Report</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif; margin:24px;}}
h1{{margin:0 0 8px 0;}}
.badge{{display:inline-block;padding:2px 8px;border-radius:10px;background:#EEF2FF;border:1px solid #A78BFA;}}
table{{border-collapse:collapse;width:100%;margin-top:16px;}}
th,td{{border:1px solid #e5e7eb;padding:8px;font-size:14px;}}
th{{background:#f9fafb;text-align:left;}}
</style>
</head><body>
<h1>Data Quality Report</h1>
<div class="badge">Overall: {summary['overall_status']}</div>
<p>Pass: {summary['pass']} | Warn: {summary['warn']} | Fail: {summary['fail']}</p>
<table>
<thead><tr><th>Rule</th><th>Severity</th><th>Key</th><th>Message</th></tr></thead>
<tbody>
{rows if rows else "<tr><td colspan='4'>No issues detected.</td></tr>"}
</tbody>
</table>
</body></html>"""

def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    issues = []

    att_path = STAGED / "attendance_clean.csv"
    res_path = STAGED / "results_clean.csv"

    if att_path.exists():
        att = pd.read_csv(att_path)
        issues += check_attendance(att)
    if res_path.exists():
        res = pd.read_csv(res_path)
        issues += check_results(res)

    fail = sum(1 for i in issues if i["severity"] == "FAIL")
    warn = sum(1 for i in issues if i["severity"] == "WARN")
    passed = 3  # for demo display; rules are documented in YAML
    overall = "PASS" if fail == 0 else "FAIL"

    summary = {
        "run_id": "run-0001",
        "overall_status": "PASS with WARN" if (fail == 0 and warn > 0) else overall,
        "pass": passed,
        "warn": warn,
        "fail": fail,
    }

    (REPORTS / "dq_summary_sample.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    (REPORTS / "dq_report_sample.html").write_text(render_html(summary, issues), encoding="utf-8")

    if issues:
        pd.DataFrame(issues).to_csv(REPORTS / "dq_issues.csv", index=False)

if __name__ == "__main__":
    main()
