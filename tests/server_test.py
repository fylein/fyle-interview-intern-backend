from sqlalchemy.exc import IntegrityError
from flask import Flask, jsonify
import pytest
from core.server import handle_error, HTTPException, FyleError, ValidationError, IntegrityError, app
from core.libs import helpers


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_ready_route(client, monkeypatch):
    # Mocking the get_utc_now function to have a predictable time
    mock_utc_now = "2022-01-01T12:00:00"
    monkeypatch.setattr(helpers, 'get_utc_now', lambda: mock_utc_now)

    # Make a request to the / route
    response = client.get('/')

    # Check the response
    assert response.status_code == 200
    assert response.json == {'status': 'ready', 'time': mock_utc_now}


def test_handle_fyle_error():
    with app.app_context():
        # Test handling FyleError
        err = FyleError(status_code=404, message="FyleError message")
        response = handle_error(err)
        print(response[0].json, "HI")

        assert response[0].json == {
            'error': 'FyleError', 'message': 'FyleError message'}
        assert response[1] == 404


def test_handle_validation_error():
    with app.app_context():
        # Test handling ValidationError
        err = ValidationError("Validation error message", status_code=400, messages={
                              'field': 'Error message'})
        response = handle_error(err)

        assert response[0].json == {
            'error': 'ValidationError', 'message': ['Validation error message']}
        assert response[1] == 400


def test_handle_http_exception():
    with app.app_context():
        # Test handling HTTPException
        http_exception = HTTPException(description="HTTP Exception message")
        http_exception.code = 404  # Set the code using the response attribute
        response = handle_error(http_exception)
        print(response[0].json, "HI")

        assert response[0].json == {
            'error': 'HTTPException', 'message': '404 Not Found: HTTP Exception message'}
        assert response[1] == 404
