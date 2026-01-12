-- Curated views for BI (Power BI friendly keys)

CREATE OR REPLACE VIEW dw.v_curated_attendance_monthly AS
SELECT
  d.year,
  d.month,
  d.month_name,
  s.class_id,
  s.class_name,
  s.student_id,
  s.roll_no,
  s.full_name,
  sub.subject_id,
  sub.subject_name,
  COUNT(*) AS total_sessions,
  SUM(CASE WHEN fa.status='Present' THEN 1 ELSE 0 END) AS present_count,
  SUM(CASE WHEN fa.status='Late' THEN 1 ELSE 0 END) AS late_count,
  SUM(CASE WHEN fa.status='Absent' THEN 1 ELSE 0 END) AS absent_count,
  SUM(fa.present_flag) AS present_or_late_count,
  ROUND(100.0 * SUM(fa.present_flag) / COUNT(*), 2) AS attendance_pct
FROM dw.fact_attendance fa
JOIN dw.dim_date d ON d.date_key = fa.date_key
JOIN dw.dim_student s ON s.student_id = fa.student_id
JOIN dw.dim_subject sub ON sub.subject_id = fa.subject_id
GROUP BY
  d.year, d.month, d.month_name,
  s.class_id, s.class_name,
  s.student_id, s.roll_no, s.full_name,
  sub.subject_id, sub.subject_name;

CREATE OR REPLACE VIEW dw.v_curated_results_term AS
SELECT
  fr.term_key,
  t.term_name,
  s.class_id,
  s.class_name,
  s.student_id,
  s.roll_no,
  s.full_name,
  SUM(fr.obtained_total) AS total_obtained,
  SUM(fr.max_total) AS total_max,
  ROUND(100.0 * SUM(fr.obtained_total) / NULLIF(SUM(fr.max_total),0), 2) AS overall_percentage,
  CASE
    WHEN SUM(CASE WHEN fr.pass_fail='Fail' THEN 1 ELSE 0 END) > 0 THEN 'Fail'
    ELSE 'Pass'
  END AS overall_pass_fail
FROM dw.fact_result fr
JOIN dw.dim_student s ON s.student_id = fr.student_id
JOIN dw.dim_term t ON t.term_key = fr.term_key
GROUP BY
  fr.term_key, t.term_name,
  s.class_id, s.class_name,
  s.student_id, s.roll_no, s.full_name;
