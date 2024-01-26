

SELECT state, COUNT(*) AS assignment_count
FROM assignments
GROUP BY state;