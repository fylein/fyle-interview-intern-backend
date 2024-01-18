-- Write query to get number of assignments for each state
SELECT 
    state, 
    COUNT(*) AS assignment_count 
FROM 
    assignments 
GROUP BY 
    state;
