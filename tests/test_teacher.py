from core.models.assignments import Teacher
from core import db, create_app

def test_repr():
    teacher = Teacher(id=1)
    assert repr(teacher) == '<Teacher 1>'

