from sqlalchemy import text
from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum

def clear_assignments():
    db.session.query(Assignment).delete()
    db.session.commit()



def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1, grade: GradeEnum = GradeEnum.A) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.
    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.
    - grade (GradeEnum): The grade to be assigned to the assignments (default is Grade A).
    Returns:
    - int: Count of assignments with the specified grade.
    """
    # Count the existing assignments with the specified grade for the specified teacher
    grade_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == grade
    ).count()

    # Create 'n' graded assignments with the specified grade
    for _ in range(number):
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='Test content',
            state=AssignmentStateEnum.GRADED
        )
        db.session.add(assignment)
        grade_counter += 1

    # Commit the assignments to the database
    db.session.commit()

    return grade_counter


def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""
    
    # Fetch all the assignments for student 1 and change their state to 'GRADED'
    assignments = Assignment.filter(Assignment.student_id == 1)
    
    # Update state of each assignment
    for assignment in assignments:
        assignment.state = AssignmentStateEnum.GRADED
    
    db.session.commit()

    # Expected result (Adjust based on the test setup)
    expected_result = [(1, 3)]

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
        sql = fo.read()
    
    sql_result = db.session.execute(text(sql)).fetchall()

    for i, result in enumerate(expected_result):
        assert result[0] == sql_result[i][0], f"Expected {result[0]}, but got {sql_result[i][0]}"


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    clear_assignments()
    """Test to get count of Grade A assignments for the teacher who has graded the most assignments"""
    
    # Step 1: Create and grade 5 assignments with Grade A for the default teacher (teacher_id=1)
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5, teacher_id=1, grade=GradeEnum.A)
    
    # Step 2: Execute the SQL query and check if the count matches the created assignments
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()
    sql_result = db.session.execute(text(sql)).fetchall()
    
    # Assert that the number of Grade A assignments matches what was created
    assert grade_a_count_1 == sql_result[0][0], f"Expected {grade_a_count_1}, but got {sql_result[0][0]}"

    # Step 3: Create and grade 10 assignments with Grade A for a different teacher (teacher_id=2)
    grade_a_count_2 = create_n_graded_assignments_for_teacher(10, teacher_id=2, grade=GradeEnum.A)

    # Step 4: Execute the SQL query again and check if the count matches the newly created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    
    # Assert that the number of Grade A assignments matches what was created for teacher 2
    assert grade_a_count_2 == sql_result[0][0], f"Expected {grade_a_count_2}, but got {sql_result[0][0]}"