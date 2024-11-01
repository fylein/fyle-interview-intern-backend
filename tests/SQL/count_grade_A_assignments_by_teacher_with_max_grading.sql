-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH TotalGrades AS (
    SELECT 
        teacher_id, 
        COUNT(*) AS total_count
    FROM 
        assignments
    GROUP BY 
        teacher_id
),
AGradeCount AS (
    SELECT 
        teacher_id, 
        COUNT(*) AS a_grade_count
    FROM 
        assignments
    WHERE 
        grade = 'A'
    GROUP BY 
        teacher_id
)
SELECT 
    agc.a_grade_count
FROM 
    TotalGrades tg
JOIN 
    AGradeCount agc 
    ON tg.teacher_id = agc.teacher_id
WHERE 
    tg.total_count = (
        SELECT 
            MAX(total_count) 
        FROM 
            TotalGrades
    );