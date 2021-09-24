import json
from flask import request
from core.libs import assertions
from functools import wraps


class Principal:
    def __init__(self, user_id, student_id=None, teacher_id=None):
        self.user_id = user_id
        self.student_id = student_id
        self.teacher_id = teacher_id


def accept_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        return func(incoming_payload, *args, **kwargs)
    return wrapper


def auth_principal(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'principal not found')
        p_dict = json.loads(p_str)
        p = Principal(
            user_id=p_dict['user_id'],
            student_id=p_dict.get('student_id'),
            teacher_id=p_dict.get('teacher_id')
        )

        if request.path.startswith('/student'):
            assertions.assert_true(p.student_id is not None, 'requester should be a student')
        elif request.path.startswith('/teacher'):
            assertions.assert_true(p.teacher_id is not None, 'requester should be a teacher')
        else:
            assertions.assert_found(None, 'No such api')

        return func(p, *args, **kwargs)
    return wrapper
