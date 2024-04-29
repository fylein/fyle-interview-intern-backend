-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT COUNT(*) AS count_grade_a  
FROM assignments AS assg
JOIN teachers AS t ON assg.teacher_id = t.id 
WHERE assg.grade = 'A'  
GROUP BY t.id  
ORDER BY count_grade_a DESC
LIMIT 1;  