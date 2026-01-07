INSERT OR IGNORE INTO classes (class_name) VALUES
('BCA-1'), ('BCA-2'), ('BCA-3');

INSERT OR IGNORE INTO subjects (subject_name, max_marks) VALUES
('DBMS', 100),
('OOP', 100),
('Networking', 100);

INSERT OR IGNORE INTO users (username, password, role) VALUES
('admin','admin','Admin');

-- Synthetic students (BCA-3)
INSERT OR IGNORE INTO students (roll_no, full_name, class_id, status) VALUES
('BCA3-001','Ayesha Patel',(SELECT class_id FROM classes WHERE class_name='BCA-3'),'Active'),
('BCA3-002','Rahul Mehta',(SELECT class_id FROM classes WHERE class_name='BCA-3'),'Active'),
('BCA3-003','Neha Shah',(SELECT class_id FROM classes WHERE class_name='BCA-3'),'Active'),
('BCA3-004','Jatin Desai',(SELECT class_id FROM classes WHERE class_name='BCA-3'),'Active'),
('BCA3-005','Riya Joshi',(SELECT class_id FROM classes WHERE class_name='BCA-3'),'Inactive'),
('BCA3-006','Vivek Kumar',(SELECT class_id FROM classes WHERE class_name='BCA-3'),'Active'),
('BCA3-007','Krisha Parmar',(SELECT class_id FROM classes WHERE class_name='BCA-3'),'Active');

-- One day attendance (2026-01-02)
INSERT OR IGNORE INTO attendance (student_id, attendance_date, present)
SELECT student_id, '2026-01-02', CASE WHEN roll_no='BCA3-003' THEN 0 ELSE 1 END
FROM students WHERE roll_no LIKE 'BCA3-%';

-- Term-1 results for DBMS (internal out of 30, external out of 70)
INSERT OR IGNORE INTO results (student_id, subject_id, term, internal_marks, external_marks, total_marks, pass_fail)
SELECT s.student_id,
       (SELECT subject_id FROM subjects WHERE subject_name='DBMS'),
       'Term-1',
       CASE s.roll_no
         WHEN 'BCA3-001' THEN 23
         WHEN 'BCA3-002' THEN 19
         WHEN 'BCA3-003' THEN 15
         WHEN 'BCA3-004' THEN 21
         WHEN 'BCA3-005' THEN 24
         WHEN 'BCA3-006' THEN 18
         ELSE 20 END,
       CASE s.roll_no
         WHEN 'BCA3-001' THEN 54
         WHEN 'BCA3-002' THEN 49
         WHEN 'BCA3-003' THEN 28
         WHEN 'BCA3-004' THEN 41
         WHEN 'BCA3-005' THEN 46
         WHEN 'BCA3-006' THEN 52
         ELSE 45 END,
       0,
       'Pass'
FROM students s WHERE s.roll_no LIKE 'BCA3-%';

-- Update totals and pass/fail (pass threshold = 40)
UPDATE results
SET total_marks = internal_marks + external_marks,
    pass_fail = CASE WHEN (internal_marks + external_marks) >= 40 THEN 'Pass' ELSE 'Fail' END
WHERE term='Term-1' AND subject_id=(SELECT subject_id FROM subjects WHERE subject_name='DBMS');
