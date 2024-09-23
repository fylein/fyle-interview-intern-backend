from core.models.assignments import AssignmentStateEnum, GradeEnum
from flask import jsonify
from core.libs.exceptions import FyleError
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
import pytest
from core import app
from core.libs import helpers
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import BadRequest, InternalServerError




@pytest.mark.parametrize("exception_type, expected_status, expected_error_type",[
   ('FyleError', 400, 'FyleError'),
    ('ValidationError', 400, 'ValidationError'),
    ('IntegrityError', 400, 'IntegrityError'),
    ('HTTPException', 400, 'BadRequest'),
])
def test_handle_errors(client, h_principal, exception_type, expected_status, expected_error_type):
    response = client.get(f'/test/error?type={exception_type}', headers=h_principal)

    print(f"Testing exception type: {exception_type}")
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.data}")


    assert response.status_code == expected_status
    assert response.json['error'] == expected_error_type 
    assert 'message' in response.json


def test_generic_exception(client, h_principal):
    response = client.get('/test/generic-error', headers=h_principal)
    
    print(f"Testing generic error")
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.data}")

    assert response.status_code == 500  # Assuming your generic exception returns a 500
    assert 'message' in response.json      



def test_ready(client, h_principal):
    response = client.get('/', headers=h_principal)

    print(f"Testing '/' endpoint")
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.json}")

    assert response.status_code == 200
    assert response.json['status'] == 'ready'
    assert 'time' in response.json  # Ensure that the response contains the time

# Test for the 'Unknown error' case in the /test/error handler
def test_unknown_error(client, h_principal):
    response = client.get('/test/error?type=UnknownError', headers=h_principal)

    print(f"Testing unknown error")
    print(f"Response status code: {response.status_code}")
    print(f"Response data: {response.data}")

    assert response.status_code == 500  # Expecting a 500 status code
    assert response.json['error'] == 'GenericError'  # Check the error type
    assert 'message' in response.json  # Ensure there's a message in the response         


