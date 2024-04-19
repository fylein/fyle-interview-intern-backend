-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT COUNT(grade) AS grade_A_count
FROM assignments
WHERE grade = 'A'
AND teacher_id = :teacher_id;
