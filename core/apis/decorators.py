import json
from flask import request
from core.libs import assertions
from functools import wraps


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
        assertions.assert_found(incoming_payload, "Payload not found")
        return func(incoming_payload, *args, **kwargs)
    return wrapper


def authenticate_principal(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'Principal not found in headers')

        try:
            p_dict = json.loads(p_str)
        except json.JSONDecodeError:
            assertions.assert_auth(False, 'Invalid principal format')

        user_id = p_dict.get('user_id')
        assertions.assert_auth(user_id is not None, 'User ID not found in principal')

        p = AuthPrincipal(
            user_id=user_id,
            student_id=p_dict.get('student_id'),
            teacher_id=p_dict.get('teacher_id'),
            principal_id=p_dict.get('principal_id')
        )

        # Ensure correct role for the API path
        if request.path.startswith('/student'):
            assertions.assert_auth(p.student_id is not None, 'Requester must be a student')
        elif request.path.startswith('/teacher'):
            assertions.assert_auth(p.teacher_id is not None, 'Requester must be a teacher')
        elif request.path.startswith('/principal'):
            assertions.assert_auth(p.principal_id is not None, 'Requester must be a principal')
        else:
            assertions.assert_found(False, 'Invalid API endpoint')

        return func(p, *args, **kwargs)
    return wrapper
