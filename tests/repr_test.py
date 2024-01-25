import pytest
from core.models.assignments import Assignment,GradeEnum,AssignmentStateEnum
from core.models.students import Student
from core.models.teachers import Teacher
# Change : tests cases for repr method in Assignment,Student,Teacher

@pytest.fixture
def sample_assignment():
    # Create a sample Assignment for testing
    return Assignment(
        student_id=1,
        content="Sample Assignment Content",
        grade=GradeEnum.A,
        state=AssignmentStateEnum.DRAFT
    )

def test_assignment_repr(sample_assignment):
    # Test the __repr__ method of the Assignment class
    expected_repr = f'<Assignment {sample_assignment.id}>'
    assert repr(sample_assignment) == expected_repr

@pytest.fixture
def sample_student():
    # Create a sample Student for testing
    return Student(user_id=1)

def test_student_repr(sample_student):
    # Test the __repr__ method of the Student class
    expected_repr = f'<Student {sample_student.id}>'
    
    assert repr(sample_student) == expected_repr

@pytest.fixture
def sample_teacher():
    # Create a sample Teacher for testing
    return Teacher(user_id=1)

def test_teacher_repr(sample_teacher):
    # Test the __repr__ method of the Teacher class
    expected_repr = f'<Teacher {sample_teacher.id}>'
    
    assert repr(sample_teacher) == expected_repr
