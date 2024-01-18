-- Write query to get number of assignments for each state
SELECT state, COUNT(*) AS StateCount
FROM assignments
GROUP BY state;