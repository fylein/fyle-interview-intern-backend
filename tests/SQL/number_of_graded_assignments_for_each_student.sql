-- Write query to get number of graded assignments for each student:
SELECT student_id, COUNT(*) AS total_graded_assignment
FROM assignments
WHERE state = 'GRADED'
GROUP BY student_id;