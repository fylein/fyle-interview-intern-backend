-- Write query to get number of assignments for each state

SELECT assignments.state AS "assignment state", 
COUNT(*) AS "number of assignments" 
from assignments 
GROUP BY assignments.state;