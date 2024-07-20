from .db import db
from .users import User
from .students import Student
from .teachers import Teacher
from .assignments import Assignment
from .principals import Principal
__all__ = ['db', 'Assignment', 'Student', 'Teacher']