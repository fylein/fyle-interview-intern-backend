from core.models.assignments import Student
from core import db, create_app

def test_repr():
    student = Student(id=1)
    assert repr(student) == '<Student 1>'

