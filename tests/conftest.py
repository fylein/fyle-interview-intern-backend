import pytest
import json
from core.server import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///./test.sqlite3'
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def h_student_1():
    return {
        'X-Principal': json.dumps({
            'student_id': 1,
            'user_id': 1
        })
    }

@pytest.fixture
def h_student_2():
    return {
        'X-Principal': json.dumps({
            'student_id': 2,
            'user_id': 2
        })
    }

@pytest.fixture
def h_teacher_1():
    return {
        'X-Principal': json.dumps({
            'teacher_id': 1,
            'user_id': 3
        })
    }

@pytest.fixture
def h_teacher_2():
    return {
        'X-Principal': json.dumps({
            'teacher_id': 2,
            'user_id': 4
        })
    }

@pytest.fixture
def h_principal():
    return {
        'X-Principal': json.dumps({
            'principal_id': 1,
            'user_id': 5
        })
    }
