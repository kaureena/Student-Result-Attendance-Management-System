## Raw Data Files

### attendance_raw.csv
Columns:
- student_id (int)
- subject_id (int)
- attendance_date (YYYY-MM-DD)
- status (Present/Absent/Late/Leave)
- remarks (text)

### result_component_raw.csv
Columns:
- student_id (int)
- subject_id (int)
- term (text, e.g. Term-1)
- component_id (int)
- marks_obtained (int)

Component Mapping:
- 1 = Theory
- 2 = Internal
- 3 = Practical
- 4 = Viva

### result_raw.csv
Columns:
- student_id (int)
- subject_id (int)
- term (text)
- obtained_total (int)
- max_total (int)
- percentage (numeric)
- pass_fail (Pass/Fail)
