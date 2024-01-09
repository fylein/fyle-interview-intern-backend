import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
    # Count the existing assignments with grade 'A' for the specified teacher
    grade_a_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    # Create 'n' graded assignments
    for _ in range(number):
        # Randomly select a grade from GradeEnum
        grade = random.choice(list(GradeEnum))

        # Create a new Assignment instance
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )

        # Add the assignment to the database session
        db.session.add(assignment)

        # Update the grade_a_counter if the grade is 'A'
        if grade == GradeEnum.A:
            grade_a_counter = grade_a_counter + 1

    # Commit changes to the database
    db.session.commit()

    # Return the count of assignments with grade 'A'
    return grade_a_counter


def test_get_assignments_in_various_states():
    """Test to get assignments in various states"""

    # Define the expected result before any changes
    expected_result = [('DRAFT', 2), ('GRADED', 2), ('SUBMITTED', 2)]

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_assignments_per_state.sql', encoding='utf8') as fo:
        sql = fo.read()

    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]
        assert result[1] == sql_result[itr][1]

    # Modify an assignment state and grade, then re-run the query and check the updated result
    expected_result = [('DRAFT', 2), ('GRADED', 3), ('SUBMITTED', 1)]

    # Find an assignment in the 'SUBMITTED' state, change its state to 'GRADED' and grade to 'C'
    submitted_assignment: Assignment = Assignment.filter(Assignment.state == AssignmentStateEnum.SUBMITTED).first()
    submitted_assignment.state = AssignmentStateEnum.GRADED
    submitted_assignment.grade = GradeEnum.C

    # Flush the changes to the database session
    db.session.flush()
    # Commit the changes to the database
    db.session.commit()

    # Execute the SQL query again and compare the updated result with the expected result
    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]
        assert result[1] == sql_result[itr][1]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    # Read the SQL query from a file
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Create and grade 5 assignments for the default teacher (teacher_id=1)
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5)
    
    # Execute the SQL query and check if the count matches the created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    assert grade_a_count_1 == sql_result[0][0]

    # Create and grade 10 assignments for a different teacher (teacher_id=2)
    grade_a_count_2 = create_n_graded_assignments_for_teacher(10, 2)

    # Execute the SQL query again and check if the count matches the newly created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    assert grade_a_count_2 == sql_result[0][0]
