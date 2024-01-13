-- Write query to get number of assignments for each state
SELECT State, COUNT(*) AS AssignmentCount
FROM Assignments
GROUP BY State;
