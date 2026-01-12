# Dataset model notes

Tables expected in the warehouse:
- dim_student, dim_subject, dim_date, dim_class
- fact_attendance, fact_results

Suggested measures:
- Attendance % = Present / Total
- Pass Rate = Pass / Total
- At-Risk Index = Low attendance AND low marks
