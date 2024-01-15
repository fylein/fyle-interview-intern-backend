-- Write query to get number of assignments for each state
SELECT state, COUNT(*) AS 'Number of Assignments'
FROM assignments
GROUP BY state;
