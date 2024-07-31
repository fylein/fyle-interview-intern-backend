-- Write query to get number of graded assignments for each student:
SELECT student_id, count(*)
FROM assignments
WHERE state IS 'GRADED'
GROUP BY student_id