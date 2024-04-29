-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
select count(grade) from assignments a where a.grade='A' and a.teacher_id in
(select teacher_id from
(SELECT t.id AS teacher_id,COUNT(a.id) AS graded_count FROM teachers t JOIN assignments a ON t.id = a.teacher_id where a.state='GRADED' GROUP BY t.id)
ORDER BY graded_count DESC LIMIT 1);