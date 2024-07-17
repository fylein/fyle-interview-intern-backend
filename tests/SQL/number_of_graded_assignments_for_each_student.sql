-- /tests/SQL/number_of_graded_assignments_for_each_student.sql
-- Write query to get number of graded assignments for each student:
SELECT student_id, COUNT(*) AS graded_assignments
FROM assignments
WHERE state = "GRADED"
GROUP BY student_id;