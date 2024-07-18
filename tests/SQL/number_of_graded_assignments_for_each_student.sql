-- Write query to get number of graded assignments for each student:
SELECT
STUDENT_ID, COUNT(*) AS GRADED_ASSIGNMENT_COUNT
FROM ASSIGNMENTS
WHERE STATE = "GRADED"
GROUP BY STUDENT_ID