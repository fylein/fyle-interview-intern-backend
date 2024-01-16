-- Write query to get number of assignments for each state
SELECT state, count(*) AS count
FROM assignments
GROUP BY state;