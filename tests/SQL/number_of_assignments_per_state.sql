-- Write query to get number of assignments for each state
SELECT state, COUNT(*) AS state_count
FROM assignments
WHERE state != 'DRAFT'  AND grade IS NOT NULL
GROUP BY state;

