-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

SELECT MAX(count) FROM(
	SELECT teacher_id, COUNT(*) AS count FROM assignments
	WHERE grade = 'A' 
	GROUP BY teacher_id
	)
