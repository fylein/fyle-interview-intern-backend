-- Write query to find the number of grade A's given by the teacher who has graded the most assignment
SELECT COUNT(*) AS num_grade_a
FROM assignments a
JOIN teachers t ON a.teacher_id = t.id
WHERE a.grade = 'A'
GROUP BY t.id
ORDER BY COUNT(*) DESC
LIMIT 1;