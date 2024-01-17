SELECT COUNT(*) AS num_grade_a
FROM assignments a
JOIN teachers t ON a.teacher_id = t.id
WHERE a.grade = 'A'
GROUP BY t.id
ORDER BY COUNT(*) DESC
LIMIT 1;