-- Write query to get number of graded assignments for each student:
SELECT student_id, COUNT(*) AS graded_assignments_count
FROM assignments
WHERE state = 'graded'
GROUP BY student_id;

WITH teacher_grading_count AS (SELECT teacher_id, COUNT(*) AS graded_assignments_count 
FROM assignments
WHERE state = 'graded'
GROUP BY teacher_id),
max_grading_teacher AS (SELECT teacher_id FROM teacher_grading_count 
ORDER BY graded_assignments_count 
DESC LIMIT 1)
SELECT COUNT(*) AS grade_a_count
FROM assignments
WHERE teacher_id = (SELECT teacher_id FROM max_grading_teacher)
AND grade = 'a';

SELECT * 
FROM assignments
WHERE student_id = 1  
AND state = 'graded';

SELECT COUNT(*) AS grade_a_count
FROM assignments
WHERE teacher_id = 1  
AND grade = 'a';

