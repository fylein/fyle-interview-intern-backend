import json
from flask import request
from core.libs import assertions
from functools import wraps
from core.models.students import Student
from core.models.teachers import Teacher
from core.models.principals import Principal

class AuthPrincipal:
    def __init__(self, user_id, student_id=None, teacher_id=None, principal_id=None):
        self.user_id = user_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.principal_id = principal_id


def accept_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        return func(incoming_payload, *args, **kwargs)
    return wrapper


def authenticate_principal(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'principal not found')
        p_dict = json.loads(p_str)
        p = AuthPrincipal(
            user_id=p_dict['user_id'],
            student_id=p_dict.get('student_id'),
            teacher_id=p_dict.get('teacher_id'),
            principal_id=p_dict.get('principal_id')
        )

        if request.path.startswith('/student'):
            assertions.assert_true(p.student_id is not None, 'requester should be a student')
            student = Student.get_by_id(p.student_id)
            assertions.assert_found(student, 'Student does not exist')
            user_id_ = student.user_id
            assertions.assert_auth(p.user_id == user_id_)
        elif request.path.startswith('/teacher'):
            assertions.assert_true(p.teacher_id is not None, 'requester should be a teacher')
            teacher = Teacher.get_by_id(p.teacher_id)
            assertions.assert_found(teacher, 'teacher does not exist')
            user_id_ = teacher.user_id
            assertions.assert_auth(p.user_id == user_id_)
        elif request.path.startswith('/principal'):
            assertions.assert_true(p.principal_id is not None, 'requester should be a principal')
            principal = Principal.get_by_id(p.principal_id)
            assertions.assert_found(principal, 'principal does not exist')
            user_id_ = principal.user_id
            assertions.assert_auth(p.user_id == user_id_)
        else:
            assertions.assert_found(None, 'No such api')

        return func(p, *args, **kwargs)
    return wrapper