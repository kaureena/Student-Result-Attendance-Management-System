-- SQLite schema for v1 baseline
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS classes (
  class_id INTEGER PRIMARY KEY AUTOINCREMENT,
  class_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS students (
  student_id INTEGER PRIMARY KEY AUTOINCREMENT,
  roll_no TEXT NOT NULL UNIQUE,
  full_name TEXT NOT NULL,
  class_id INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'Active',
  FOREIGN KEY(class_id) REFERENCES classes(class_id)
);

CREATE TABLE IF NOT EXISTS subjects (
  subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject_name TEXT NOT NULL UNIQUE,
  max_marks INTEGER NOT NULL DEFAULT 100
);

CREATE TABLE IF NOT EXISTS attendance (
  attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  attendance_date TEXT NOT NULL, -- YYYY-MM-DD
  present INTEGER NOT NULL CHECK(present IN (0,1)),
  UNIQUE(student_id, attendance_date),
  FOREIGN KEY(student_id) REFERENCES students(student_id)
);

CREATE TABLE IF NOT EXISTS results (
  result_id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  subject_id INTEGER NOT NULL,
  term TEXT NOT NULL DEFAULT 'Term-1',
  internal_marks INTEGER NOT NULL CHECK(internal_marks BETWEEN 0 AND 30),
  external_marks INTEGER NOT NULL CHECK(external_marks BETWEEN 0 AND 70),
  total_marks INTEGER NOT NULL,
  pass_fail TEXT NOT NULL CHECK(pass_fail IN ('Pass','Fail')),
  FOREIGN KEY(student_id) REFERENCES students(student_id),
  FOREIGN KEY(subject_id) REFERENCES subjects(subject_id),
  UNIQUE(student_id, subject_id, term)
);

CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'Admin'
);
