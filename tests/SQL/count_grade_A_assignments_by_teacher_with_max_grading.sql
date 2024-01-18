-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT 
    teacher_id, 
    COUNT(grade) AS count_of_A_assignments
FROM 
    assignments
WHERE 
    grade = 'A'
GROUP BY 
    teacher_id;
