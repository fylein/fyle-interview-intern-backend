from core.server import handle_error
from core.libs.exceptions import FyleError
from marshmallow.exceptions import ValidationError
from flask import Flask
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError


def test_ready_endpoint(client, mocker):
    response = client.get('/')
    assert response.status_code == 200
    data = response.json

    assert data['status'] == 'ready'
    assert 'time' in data

def test_error_handler():

    app = Flask(__name__)

    class TestError(Exception):
        def __init__(self, message, status_code):
            self.message = message
            self.status_code = status_code
        

    with app.app_context():
        response_fyle_error = handle_error(FyleError('TestError', 'test error'))
        response_validation_error = handle_error(ValidationError('TestError', 'test error'))
        response_integrity_error = handle_error(IntegrityError('TestError', 'test error', 'test error'))
        response_http_exception = handle_error(HTTPException("TestError",response=None))
        try:
            response_test_error = handle_error(TestError('TestError', 'test error'))
        except Exception as e:
            response_test_error = e

    assert response_fyle_error[1] == "TestError"
    assert response_validation_error[1] == 400
    assert response_integrity_error[1] == 400
    assert response_http_exception[1] == None
    assert response_test_error.message == 'TestError'
    

    