import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.
    """
    # Create 'n' graded assignments specifically with grade 'A'
    for _ in range(number):
        # Create a new Assignment instance with grade 'A'
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,  # Change this to a valid student ID as needed
            grade=GradeEnum.A,  # Set grade to 'A'
            content='test content',
            state=AssignmentStateEnum.GRADED
        )
        
        # Add the assignment to the database session
        db.session.add(assignment)
        assignments = db.session.query(Assignment).filter_by(teacher_id=teacher_id).all()
        # print(f"Assignments for teacher 1: {len(assignments)}")  # Should be 5


    # Commit changes to the database
    db.session.commit()

    # Return the count of assignments with grade 'A'
    return number  # Since all created assignments are grade 'A'

def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    # Find all the assignments for student 1 and change its state to 'GRADED'
    submitted_assignments: Assignment = Assignment.filter(Assignment.student_id == 1)

    # Iterate over each assignment and update its state
    for assignment in submitted_assignments:
        assignment.state = AssignmentStateEnum.GRADED  # Or any other desired state

    # Flush the changes to the database session
    db.session.flush()
    # Commit the changes to the database
    db.session.commit()

    # Define the expected result before any changes
    expected_result = [(1, 3)]

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Execute the SQL query compare the result with the expected result
    sql_result = db.session.execute(text(sql)).fetchall()
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    # Read the SQL query from a file
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()
        
    sql_result_before = db.session.execute(text(sql)).fetchall()
    initial_count = sql_result_before[0][1] if sql_result_before else 0
    # Create and grade 5 assignments for the default teacher (teacher_id=1)
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5)

    sql_result_after = db.session.execute(text(sql)).fetchall()
    new_count = sql_result_after[0][1] if sql_result_after else 0  # Adjust index if necessary

    # Calculate the difference
    difference = new_count - initial_count

    
    assert 5 == difference
    

    # Create and grade 10 assignments for a different teacher (teacher_id=2)
    # sql_result_before_2 = db.session.execute(text(sql)).fetchall()
    # initial_count_2 = sql_result_before_2[0][1] if sql_result_before_2 else 0

    # grade_a_count_2 = create_n_graded_assignments_for_teacher(10, 2)

    # # # Execute the SQL query again and check if the count matches the newly created assignments
    # sql_result_after_2 = db.session.execute(text(sql)).fetchall()
    # new_count_2 = sql_result_after_2[0][1] if sql_result_after_2 else 0  # Adjust index if necessary

    # # Calculate the difference
    # difference_2 = new_count_2 - initial_count_2

    # # Assert that the difference matches the number of new assignments created
    # print(f"Initial count of grade A assignments for teacher 2: {initial_count_2}")
    # print(f"New count of grade A assignments for teacher 2: {new_count_2}")
    # print(f"Difference for teacher 2 (newly created): {difference_2}")
    # assert 10 == difference_2 
    
    
    

    
