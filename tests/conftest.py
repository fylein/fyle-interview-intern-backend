import pytest
import json
from tests import app
import shutil
import os

# Change while original database is changing... 
# So first copy original database...run tests and roll back to copy of original database.

# Define the path to the original and testing database files
original_db_path = os.path.join(os.path.dirname(__file__), '../core/store.sqlite3')
copy_db_path = os.path.join(os.path.dirname(__file__), 'copy_db.sqlite3')
@pytest.fixture(scope='session', autouse=True)
def setup_database():
    # Copy the original database file for testing
    shutil.copy(original_db_path, copy_db_path)
    
    yield  # Continue with the tests
    
    # Rollback the database to the original state after tests
    shutil.copy(copy_db_path, original_db_path)




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
