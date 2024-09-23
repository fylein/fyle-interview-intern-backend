-- select student_id, count(id) as graded_assignments from assignments where state=='GRADED';
SELECT student_id, COUNT(*) AS graded_assignments_count
FROM assignments
WHERE state = 'GRADED'
GROUP BY student_id;
