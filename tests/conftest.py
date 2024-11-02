import pytest
import json
from tests import app


@pytest.fixture(scope="function")
def client():
    """A test client for making requests in tests."""

    with app.test_client() as client:
        yield client  # Provide the test client to the tests


@pytest.fixture
def h_student_1():
    headers = {"X-Principal": json.dumps({"student_id": 1, "user_id": 1})}

    return headers


@pytest.fixture
def h_student_2():
    headers = {"X-Principal": json.dumps({"student_id": 2, "user_id": 2})}

    return headers


@pytest.fixture
def h_teacher_1():
    headers = {"X-Principal": json.dumps({"teacher_id": 1, "user_id": 3})}

    return headers


@pytest.fixture
def h_teacher_2():
    headers = {"X-Principal": json.dumps({"teacher_id": 2, "user_id": 4})}

    return headers


@pytest.fixture
def h_principal():
    headers = {"X-Principal": json.dumps({"principal_id": 1, "user_id": 5})}

    return headers
