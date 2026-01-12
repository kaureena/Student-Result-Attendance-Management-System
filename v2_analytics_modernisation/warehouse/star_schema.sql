-- Star schema (Warehouse)
CREATE TABLE IF NOT EXISTS dim_student (
  student_key INTEGER PRIMARY KEY AUTOINCREMENT,
  roll_no TEXT UNIQUE NOT NULL,
  student_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_subject (
  subject_key INTEGER PRIMARY KEY AUTOINCREMENT,
  subject_name TEXT UNIQUE NOT NULL,
  max_marks INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_date (
  date_key INTEGER PRIMARY KEY, -- YYYYMMDD
  full_date TEXT NOT NULL,
  month INTEGER NOT NULL,
  year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_class (
  class_key INTEGER PRIMARY KEY AUTOINCREMENT,
  class_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_attendance (
  student_key INTEGER NOT NULL,
  date_key INTEGER NOT NULL,
  class_key INTEGER NOT NULL,
  present_flag INTEGER NOT NULL,
  PRIMARY KEY(student_key, date_key, class_key)
);

CREATE TABLE IF NOT EXISTS fact_results (
  student_key INTEGER NOT NULL,
  subject_key INTEGER NOT NULL,
  date_key INTEGER NOT NULL,
  class_key INTEGER NOT NULL,
  term TEXT NOT NULL,
  internal_marks INTEGER NOT NULL,
  external_marks INTEGER NOT NULL,
  total_marks INTEGER NOT NULL,
  pass_fail TEXT NOT NULL,
  PRIMARY KEY(student_key, subject_key, date_key, class_key, term)
);


-- Added in v2.1: component-wise assessment model
-- See: dim/dim_assessment_component.sql and fact/fact_result_component_marks.sql
