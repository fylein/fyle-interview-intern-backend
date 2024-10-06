import pytest
import json
from tests import app
from core import db  
from core.models.assignments import Assignment  

@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def h_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

    return headers


@pytest.fixture
def h_student_2():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

    return headers

@pytest.fixture
def h_student_3():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 1
        })
    }

    return headers


@pytest.fixture
def h_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }

    return headers


@pytest.fixture
def h_teacher_2():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }

    return headers


@pytest.fixture
def h_teacher_3():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 7,
            'user_id': 10
        })
    }

    return headers


@pytest.fixture
def h_principal():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }

    return headers


@pytest.fixture
def h_principal_1():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 3,
            'user_id': 5
        })
    }

    return headers



