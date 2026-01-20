# v1 Test Matrix (Manual)

| Test ID | Module | Scenario | Input | Expected result | Evidence path |
|---|---|---|---|---|---|
| V1-T01 | Students | Duplicate roll number | roll_no repeated | Reject with error | src/student_module.py |
| V1-T02 | Attendance | Unknown roll number | roll_no=UNKNOWN | Reject | src/attendance_module.py |
| V1-T03 | Results | Invalid marks | marks too high | Validation error | src/result_module.py |
| V1-T04 | Exports | Results export | class=BCA-3 | XLSX created | export/result_report_sample.xlsx |
