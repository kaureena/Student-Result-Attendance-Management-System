-- Fact: component-wise marks (supports Theory/Practical/Viva/etc.)
CREATE TABLE IF NOT EXISTS fact_result_component_marks (
  student_key INT NOT NULL,
  subject_key INT NOT NULL,
  date_key INT NOT NULL,
  class_key INT NOT NULL,
  component_key INT NOT NULL,
  term TEXT NOT NULL,
  marks_obtained INT NOT NULL,
  max_marks INT NOT NULL
);
