SELECT COUNT(*) AS grade_A_count
FROM assignments a
JOIN teachers t ON a.teacher_id = t.id
WHERE a.grade = 'A' AND a.state = 'GRADED'
GROUP BY t.id
ORDER BY COUNT(*) DESC
LIMIT 1;
