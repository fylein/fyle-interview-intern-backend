-- Write query to get number of graded assignments for each student:

SELECT s.name, COUNT(DISTINCT g.assignment_id) AS num_graded_assignments
FROM Students s
JOIN Submissions sub ON s.id = sub.student_id
JOIN Grades g ON sub.id = g.submission_id
GROUP BY s.name;
