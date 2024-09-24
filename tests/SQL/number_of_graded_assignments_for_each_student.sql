
SELECT student_id, COUNT(*) as graded_assignments
FROM assignments
WHERE grade IS NOT NULL
GROUP BY student_id;
