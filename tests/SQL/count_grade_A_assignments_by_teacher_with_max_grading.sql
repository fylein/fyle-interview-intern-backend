-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

SELECT COUNT(*) 
FROM assignments 
WHERE grade = 'A' 
AND teacher_id = :teacher_id
GROUP BY teacher_id;