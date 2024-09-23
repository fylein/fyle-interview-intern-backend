-- Write query to get number of graded assignments for each student
SELECT COUNT(state) as count
FROM assignments
WHERE assignments.state = 'GRADED'
GROUP BY student_id
ORDER BY count ASC;