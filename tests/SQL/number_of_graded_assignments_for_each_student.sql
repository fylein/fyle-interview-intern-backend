-- query to get number of graded assignments for each student:
SELECT student_id, COUNT(*) AS graded_assignments_count
FROM assignments
-- Filter assignments with state GRADED
WHERE state = 'GRADED'
-- Group the assignments by student_id
GROUP BY student_id;
