-- PostgreSQL OLTP schema (v2) - updated for component-wise marks

CREATE TABLE IF NOT EXISTS classes (
  class_id   SERIAL PRIMARY KEY,
  class_name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
  student_id SERIAL PRIMARY KEY,
  roll_no    TEXT NOT NULL,
  full_name  TEXT NOT NULL,
  class_id   INT  NOTcerNULL REFERENCES classes(class_id) ON DELETE RESTRICT,
  status     TEXT NOT NULL DEFAULT 'Active'
    CHECK (status IN ('Active','Inactive','Left')),
  UNIQUE (class_id, roll_no)
);


CREATE TABLE IF NOT EXISTS subjects (
  subject_id   SERIAL PRIMARY KEY,
  subject_name TEXT UNIQUE NOT NULL
);


-- Which subjects are taught in which class
CREATE TABLE IF NOT EXISTS class_subjects (
  class_id   INT NOT NULL REFERENCES classes(class_id) ON DELETE CASCADE,
  subject_id INT NOT NULL REFERENCES subjects(subject_id) ON DELETE RESTRICT,
  PRIMARY KEY (class_id, subject_id)
);

-- Components like Theory/Internal/Practical/Viva
CREATE TABLE IF NOT EXISTS assessment_components (
  component_id   SERIAL PRIMARY KEY,
  component_name TEXT UNIQUE NOT NULL
);

-- Per-subject config: decides total max (100/200 etc.)
CREATE TABLE IF NOT EXISTS subject_assessment_components (
  subject_id    INT NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
  component_id  INT NOT NULL REFERENCES assessment_components(component_id) ON DELETE RESTRICT,
  max_marks     INT NOT NULL CHECK (max_marks > 0),
  min_marks     INT NOT NULL DEFAULT 0 CHECK (min_marks >= 0),
  display_order INT NOT NULL DEFAULT 1 CHECK (display_order > 0),
  PRIMARY KEY (subject_id, component_id),
  CHECK (min_marks <= max_marks)
);

---Subject-wise attendance (one row per student + subject + date)
CREATE TABLE IF NOT EXISTS attendance (
  attendance_id  SERIAL PRIMARY KEY,
  student_id     INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
  subject_id     INT NOT NULL REFERENCES subjects(subject_id) ON DELETE RESTRICT,
  attendance_date DATE NOT NULL,
  status         TEXT NOT NULL CHECK (status IN ('Present','Absent','Late'),
  remarks        TEXT,

  -- Prevent duplicate attendance for same student, subject, date
  UNIQUE (student_id, subject_id, attendance_date)
);


-- RESULTS (TERM-WISE)
-- =========================

-- "Header" row per student+subject+term (publish/remarks etc.)
CREATE TABLE IF NOT EXISTS results (
  result_id  SERIAL PRIMARY KEY,
  student_id INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
  subject_id INT NOT NULL REFERENCES subjects(subject_id) ON DELETE RESTRICT,
  term       TEXT NOT NULL CHECK (term IN ('Term-1','Final')),
  published  BOOLEAN NOT NULL DEFAULT FALSE,
  remarks    TEXT,
  UNIQUE (student_id, subject_id, term)
);


-- Component marks per student+subject+term
CREATE TABLE IF NOT EXISTS result_component_marks (
  student_id     INT NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
  subject_id     INT NOT NULL REFERENCES subjects(subject_id) ON DELETE RESTRICT,
  term           TEXT NOT NULL CHECK (term IN ('Term-1','Final')),
  component_id   INT NOT NULL REFERENCES assessment_components(component_id) ON DELETE RESTRICT,
  marks_obtained INT NOT NULL CHECK (marks_obtained >= 0),
  PRIMARY KEY (student_id, subject_id, term, component_id),

  -- Only allow components that are configured for that subject
  FOREIGN KEY (subject_id, component_id)
    REFERENCES subject_assessment_components(subject_id, component_id)
);
