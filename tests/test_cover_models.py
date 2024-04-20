import pytest
from core.models.students import Student
from core.models.teachers import Teacher
from core.models.assignments import Assignment, AssignmentStateEnum, assertions


def test_student_repr():
    # Create a student instance for testing
    student = Student(id=1)

    # Check the representation string
    repr_string = repr(student)

    # Assert that the representation string contains the expected format
    assert repr_string.startswith('<Student 1')


def test_teacher_repr():
    # Create a teacher instance for testing
    teacher = Teacher(id=1)

    # Check the representation string
    repr_string = repr(teacher)

    # Assert that the representation string contains the expected format
    assert repr_string.startswith('<Teacher 1')


@pytest.fixture
def sample_assignment():
    # Create a sample assignment for testing
    return Assignment(student_id=1, content='Sample Content')


def test_assignment_repr(sample_assignment):
    # Check the __repr__ method of the Assignment class
    repr_string = repr(sample_assignment)
    assert repr_string.startswith('<Assignment ')


def test_get_assignments_submitted_or_graded():
    # Create submitted and graded assignments for testing
    submitted_assignment = Assignment(
        student_id=1, content='Submitted Content', state=AssignmentStateEnum.SUBMITTED)
    graded_assignment = Assignment(
        student_id=1, content='Graded Content', state=AssignmentStateEnum.GRADED)

    # Save the assignments to the database
    submitted_assignment.upsert(submitted_assignment)
    graded_assignment.upsert(graded_assignment)

    # Retrieve assignments that are submitted or graded
    assignments = Assignment.get_assignments_submitted_or_graded()

    # Check that the assignments list contains the submitted and graded assignments
    assert submitted_assignment in assignments
    assert graded_assignment in assignments


def test_upsert_existing_assignment_with_id_check(monkeypatch):
    # Mocked function that raises AssertionError
    def mock_assert_valid(condition, error_message):
        raise AssertionError(error_message)

    # Replace the actual assert_valid function with the mocked one
    monkeypatch.setattr(assertions, 'assert_valid', mock_assert_valid)

    # Create an existing assignment with an ID
    existing_assignment = Assignment(
        student_id=3, content='Existing Assignment Content', id=1)

    # Call the upsert method, which will trigger the AssertionError
    with pytest.raises(AssertionError):
        Assignment.upsert(existing_assignment)
