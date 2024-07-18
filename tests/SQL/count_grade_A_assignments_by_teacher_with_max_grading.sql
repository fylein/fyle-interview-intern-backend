-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
-- Get the count of grade 'A' assignments for the teacher who has graded the maximum assignments
WITH TeacherGradingCounts AS (
    SELECT teacher_id, COUNT(*) AS grading_count
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),
MaxGradingTeacher AS (
    SELECT teacher_id
    FROM TeacherGradingCounts
    ORDER BY grading_count DESC
    LIMIT 1
)
SELECT COUNT(*)
FROM assignments
WHERE grade = 'A'
AND teacher_id = (SELECT teacher_id FROM MaxGradingTeacher);
