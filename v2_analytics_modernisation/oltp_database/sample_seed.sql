-- Reference seed data (PostgreSQL)
INSERT INTO classes (class_name)
VALUES ('BCA 1st Year');


INSERT INTO students (roll_no, full_name, class_id, status)
VALUES
('01','Student A',1,'Active'),
('02','Student B',1,'Active'),
('03','Student C',1,'Active');


INSERT INTO subjects (subject_name)
VALUES
('Mathematics'),
('Programming'),
('Statistics');

INSERT INTO class_subjects (class_id, subject_id)
VALUES
(1,1),(1,2),(1,3);



INSERT INTO assessment_components (component_name)
VALUES
('Theory'),
('Internal'),
('Practical'),
('Viva');


INSERT INTO subject_assessment_components
(subject_id, component_id, max_marks, min_marks, display_order)
VALUES
(1,1,70,0,1), -- Theory
(1,2,30,0,2), -- Internal
(1,3,0,0,3),  -- Practical
(1,4,0,0,4);


INSERT INTO subject_assessment_components
(subject_id, component_id, max_marks, min_marks, display_order)
VALUES
(1, (SELECT component_id FROM assessment_components WHERE component_name='Theory'),   70, 0, 1),
(1, (SELECT component_id FROM assessment_components WHERE component_name='Internal'), 30, 0, 2);



INSERT INTO subject_assessment_components
(subject_id, component_id, max_marks, min_marks, display_order)
VALUES
(2, (SELECT component_id FROM assessment_components WHERE component_name='Theory'),   70, 0, 1),
(2, (SELECT component_id FROM assessment_components WHERE component_name='Internal'), 30, 0, 2),
(2, (SELECT component_id FROM assessment_components WHERE component_name='Practical'),70, 0, 3),
(2, (SELECT component_id FROM assessment_components WHERE component_name='Viva'),     30, 0, 4);



INSERT INTO subject_assessment_components
(subject_id, component_id, max_marks, min_marks, display_order)
VALUES
(3, (SELECT component_id FROM assessment_components WHERE component_name='Theory'),   70, 0, 1),
(3, (SELECT component_id FROM assessment_components WHERE component_name='Internal'), 30, 0, 2);





INSERT INTO result_component_marks (student_id, subject_id, term, component_id, marks_obtained)
VALUES
-- Mathematics (Theory+Internal)
(1,1,'Term-1', 1, 55),
(1,1,'Term-1', 2, 25),

-- Programming (All 4)
(1,2,'Term-1', 1, 60),
(1,2,'Term-1', 2, 25),
(1,2,'Term-1', 3, 58),
(1,2,'Term-1', 4, 24),

-- Statistics (Theory+Internal)
(1,3,'Term-1', 1, 52),
(1,3,'Term-1', 2, 24);



INSERT INTO result_component_marks (student_id, subject_id, term, component_id, marks_obtained)
VALUES
-- Mathematics (Theory+Internal)
(2,1,'Term-1', 1, 40),
(2,1,'Term-1', 2, 18),

-- Programming (All 4) - low marks
(2,2,'Term-1', 1, 35),
(2,2,'Term-1', 2, 15),
(2,2,'Term-1', 3, 30),
(2,2,'Term-1', 4, 12),

-- Statistics (Theory+Internal)
(2,3,'Term-1', 1, 42),
(2,3,'Term-1', 2, 16);




INSERT INTO result_component_marks (student_id, subject_id, term, component_id, marks_obtained)
VALUES
-- Mathematics (Theory+Internal)
(3,1,'Term-1', 1, 25),
(3,1,'Term-1', 2, 10),

-- Programming (All 4) - very low
(3,2,'Term-1', 1, 20),
(3,2,'Term-1', 2, 8),
(3,2,'Term-1', 3, 20),
(3,2,'Term-1', 4, 8),

-- Statistics (Theory+Internal)
(3,3,'Term-1', 1, 28),
(3,3,'Term-1', 2, 12);



INSERT INTO attendance (student_id, subject_id, attendance_date, status)
VALUES
(1,1,'2026-01-02','Present'), (1,2,'2026-01-02','Present'), (1,3,'2026-01-02','Present'),
(1,1,'2026-01-03','Present'), (1,2,'2026-01-03','Late'),    (1,3,'2026-01-03','Present'),
(1,1,'2026-01-04','Present'), (1,2,'2026-01-04','Present'), (1,3,'2026-01-04','Present'),
(1,1,'2026-01-05','Present'), (1,2,'2026-01-05','Present'), (1,3,'2026-01-05','Present');



INSERT INTO attendance (student_id, subject_id, attendance_date, status)
VALUES
(2,1,'2026-01-02','Present'), (2,2,'2026-01-02','Absent'),  (2,3,'2026-01-02','Present'),
(2,1,'2026-01-03','Absent'),  (2,2,'2026-01-03','Present'), (2,3,'2026-01-03','Present'),
(2,1,'2026-01-04','Present'), (2,2,'2026-01-04','Absent'),  (2,3,'2026-01-04','Absent'),
(2,1,'2026-01-05','Present'), (2,2,'2026-01-05','Present'), (2,3,'2026-01-05','Absent');



INSERT INTO attendance (student_id, subject_id, attendance_date, status)
VALUES
(3,1,'2026-01-02','Absent'),  (3,2,'2026-01-02','Absent'),  (3,3,'2026-01-02','Present'),
(3,1,'2026-01-03','Absent'),  (3,2,'2026-01-03','Absent'),  (3,3,'2026-01-03','Absent'),
(3,1,'2026-01-04','Present'), (3,2,'2026-01-04','Absent'),  (3,3,'2026-01-04','Absent'),
(3,1,'2026-01-05','Absent'),  (3,2,'2026-01-05','Absent'),  (3,3,'2026-01-05','Absent');

--Results header (Term-1)

INSERT INTO results (student_id, subject_id, term, published)
SELECT s.student_id, sub.subject_id, 'Term-1', TRUE
FROM students s
CROSS JOIN subjects sub;