-- -- Write query to find the number of grade A's given by the teacher who has graded the most assignments
-- 	Select Count(*) from assignments where teacher_id in (Select teacher_id from (Select teacher_id, COUNT(*) GRADING_COUNT from assignments where state='GRADED' GROUP BY teacher_id ORDER BY GRADING_COUNT DESC limit 1)) and grade='A';
SELECT COUNT(*) AS grade_a
FROM assignments AS a
JOIN teachers AS t ON a.teacher_id = t.id
WHERE a.grade = 'A'
GROUP BY t.id
ORDER BY grade_a DESC
LIMIT 1;