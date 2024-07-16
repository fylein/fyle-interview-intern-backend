import pytest
import json
from tests import app


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
def h_bad_student():
    # Replace with logic to provide headers or setup for a bad student scenario
    return {
        'Authorization': 'Bearer your_token_here'
        # Add other headers or setup as needed
    }


@pytest.fixture
def h_bad_student_1():
    headers = {
        'X-Principal': json.dumps({
            'student_id': 100000,
            'user_id': 10
        })
    }

    return headers


@pytest.fixture
def h_bad_teacher_1():
    headers = {
        'X-Principal': json.dumps({
            'teacher_id': 100000,
            'user_id': 3
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
def h_principal():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }

    return headers


@pytest.fixture
def h_principal_bad():
    headers = {
        'X-Principal': json.dumps({
            'principal_id': 10000,
            'user_id': 5
        })
    }

    return headers
