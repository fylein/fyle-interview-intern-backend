import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


class TestSQL:

    def create_n_graded_assignments_for_teacher_and_student(self, number: int = 0, teacher_id: int = 1, student_id: int = 1) -> int:
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
                student_id=student_id,
                grade=grade,
                content='test content',
                state=AssignmentStateEnum.GRADED
            )

            # Add the assignment to the database session
            db.session.add(assignment)

            # Update the grade_a_counter if the grade is 'A'
            if grade == GradeEnum.A:
                grade_a_counter = grade_a_counter + 1

        db.session.flush()

        # Return the count of assignments with grade 'A'
        return grade_a_counter

    def test_count_assignments_in_each_grade(self):
        """Test to get count of assignments for each grade"""

        # Create 25 graded assignments for student 1
        self.create_n_graded_assignments_for_teacher_and_student(25, student_id=1)
        
        # Create 20 graded assignments for student 1
        self.create_n_graded_assignments_for_teacher_and_student(20, student_id=2)

        # Define the expected results
        expected_result = []
        for grade in list(GradeEnum):
            grade_count: int = Assignment.filter(
                Assignment.grade == grade,
                Assignment.state == AssignmentStateEnum.GRADED
            ).count()
            expected_result.append((grade.value, grade_count))

        # Execute the SQL query and compare the result with the expected result
        with open('tests/SQL/count_assignments_in_each_grade.sql', encoding='utf8') as fo:
            sql = fo.read()

        # Execute the SQL query compare the result with the expected result
        sql_result = db.session.execute(text(sql)).fetchall()
        for itr, result in enumerate(expected_result):
            assert result[0] == sql_result[itr][0]

    def test_get_grade_A_assignments_for_teacher_with_max_grading(self):
        """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

        # Read the SQL query from a file
        with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
            sql = fo.read()

        # Create and grade 5 assignments for the default teacher (teacher_id=1)
        grade_a_count_1 = self.create_n_graded_assignments_for_teacher_and_student(5)
        
        # Execute the SQL query and check if the count matches the created assignments
        sql_result = db.session.execute(text(sql)).fetchall()
        assert grade_a_count_1 == sql_result[0][0]

        # Create and grade 10 assignments for a different teacher (teacher_id=2)
        grade_a_count_2 = self.create_n_graded_assignments_for_teacher_and_student(10, 2)

        # Execute the SQL query again and check if the count matches the newly created assignments
        sql_result = db.session.execute(text(sql)).fetchall()
        assert grade_a_count_2 == sql_result[0][0]

    def teardown_method(self) -> None:
        # Rollback the changes to the database after each test
        db.session.rollback()
