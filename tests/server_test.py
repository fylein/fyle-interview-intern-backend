# /tests/server_test.py
import pytest
from flask import jsonify
from core import app
from core.libs.exceptions import FyleError
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException, InternalServerError

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_ready_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.json
    assert data['status'] == 'ready'
    assert 'time' in data

def test_handle_validation_error(client):
    @app.route('/validation_error')
    def validation_error_route():
        raise ValidationError(['Validation error occurred'])

    response = client.get('/validation_error')
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'ValidationError'
    assert data['message'] == ['Validation error occurred']

def test_handle_integrity_error(client):
    @app.route('/integrity_error')
    def integrity_error_route():
        raise IntegrityError('Integrity error occurred', 'statement', 'params')

    response = client.get('/integrity_error')
    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'IntegrityError'
    assert 'params' in data['message']  # Adjust this assertion based on actual error message structure

def test_handle_http_exception(client):
    @app.route('/http_exception')
    def http_exception_route():
        raise InternalServerError('HTTP error occurred')

    response = client.get('/http_exception')
    assert response.status_code == 500  # Adjust based on the specific HTTPException
    data = response.json
    assert data['error'] == 'InternalServerError'
    assert data['message'] == '500 Internal Server Error: HTTP error occurred'