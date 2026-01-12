-- OLTP view: term-wise results summary (use for extraction)

CREATE OR REPLACE VIEW public.v_result_summary AS
WITH obtained AS (
  SELECT
    rcm.student_id,
    rcm.subject_id,
    rcm.term,
    SUM(rcm.marks_obtained) AS obtained_total
  FROM public.result_component_marks rcm
  GROUP BY rcm.student_id, rcm.subject_id, rcm.term
),
max_tot AS (
  SELECT
    sac.subject_id,
    SUM(sac.max_marks) AS max_total
  FROM public.subject_assessment_components sac
  GROUP BY sac.subject_id
)
SELECT
  r.student_id,
  r.subject_id,
  r.term,
  o.obtained_total,
  m.max_total,
  ROUND((o.obtained_total::numeric / NULLIF(m.max_total,0)) * 100, 2) AS percentage,
  CASE
    WHEN (o.obtained_total::numeric / NULLIF(m.max_total,0)) * 100 >= 40 THEN 'Pass'
    ELSE 'Fail'
  END AS pass_fail,
  r.published
FROM public.results r
JOIN obtained o
  ON o.student_id=r.student_id AND o.subject_id=r.subject_id AND o.term=r.term
JOIN max_tot m
  ON m.subject_id=r.subject_id;
