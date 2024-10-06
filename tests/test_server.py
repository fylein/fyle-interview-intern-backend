import pytest
from core.server import app
from core.libs.exceptions import FyleError
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound, BadRequest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """
    Test the root endpoint to ensure the app is running.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['message'] == "App is running"



def test_http_exception_handler(client):
    """
    Test that HTTPException is handled correctly.
    """
    from werkzeug.exceptions import NotFound

    @app.route('/trigger-http-exception')
    def trigger_http_exception():
        raise NotFound('Resource not found')

    response = client.get('/trigger-http-exception')
    assert response.status_code == 404
    assert response.json['error'] == 'NotFound'
    assert response.json['message'] == '404 Not Found: Resource not found'



def test_uncaught_exception_handler(client):
    """
    Test that uncaught exceptions are handled correctly.
    """
    @app.route('/trigger-uncaught-exception')
    def trigger_uncaught_exception():
        raise Exception('Uncaught exception')

    try:
        response = client.get('/trigger-uncaught-exception')
    except Exception as e:
        assert str(e) == 'Uncaught exception'



def test_fyle_error_handler(client):
    """
    Test that FyleError is handled correctly.
    """
    @app.route('/trigger-fyle-error')
    def trigger_fyle_error():
        raise FyleError(500, "This is a FyleError")

    response = client.get('/trigger-fyle-error')
    assert response.status_code == 500
    assert response.json['error'] == 'FyleError'
    assert response.json['message'] == "This is a FyleError"


def test_validation_error_handler(client):
    """
    Test that ValidationError is handled correctly.
    """
    @app.route('/trigger-validation-error')
    def trigger_validation_error():
        raise ValidationError({"field": ["Invalid input."]})

    response = client.get('/trigger-validation-error')
    assert response.status_code == 400
    assert response.json['error'] == 'ValidationError'
    assert response.json['message'] == {'field': ['Invalid input.']}


def test_integrity_error_handler(client):
    """
    Test that IntegrityError is handled correctly.
    """
    @app.route('/trigger-integrity-error')
    def trigger_integrity_error():
        raise IntegrityError("Integrity constraint violation", orig=None, params={})

    response = client.get('/trigger-integrity-error')
    assert response.status_code == 400
    assert response.json['error'] == 'IntegrityError'
    assert response.json['message'] == 'Integrity constraint violation'


def test_empty_response(client):
    """
    Test that a valid request returns an empty response correctly.
    """
    @app.route('/trigger-empty-response')
    def trigger_empty_response():
        return '', 204  # No content

    response = client.get('/trigger-empty-response')
    assert response.status_code == 204
    assert response.data == b''


def test_not_found_handler(client):
    """
    Test that NotFound is handled correctly.
    """
    @app.route('/trigger-not-found')
    def trigger_not_found():
        raise NotFound('This resource does not exist')

    response = client.get('/trigger-not-found')
    assert response.status_code == 404
    assert response.json['error'] == 'NotFound'
    assert response.json['message'] == '404 Not Found: This resource does not exist'



def test_bad_request_handler(client):
    """
    Test that BadRequest is handled correctly.
    """
    @app.route('/trigger-bad-request')
    def trigger_bad_request():
        raise BadRequest('Bad Request')

    response = client.get('/trigger-bad-request')
    assert response.status_code == 400
    assert response.json['error'] == 'BadRequest'
    assert response.json['message'] == '400 Bad Request: Bad Request'


