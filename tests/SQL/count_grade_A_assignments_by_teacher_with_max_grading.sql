-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
select COUNT(*) AS grade_a from assignments a join teachers t ON a.teacher_id = t.id where a.grade = 'A' group by t.id order by COUNT(*) desc limit 1;
