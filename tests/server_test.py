import pytest
from core.server import app


def test_get_assignments_student_2(client):
    response = client.get("/")
    assert response.status_code == 200


def test_simulate_validation_error(client):
    response = client.get("/errors/simulate_validation_error")
    assert response.status_code == 400
    assert response.json["error"] == "ValidationError"


def test_simulate_integrity_error(client):
    response = client.get("/errors/simulate_integrity_error")
    assert response.status_code == 400
    assert response.json["error"] == "IntegrityError"


def test_simulate_http_exception(client):
    response = client.get("/errors/simulate_http_exception")
    assert response.status_code == 404
    assert response.json["error"] == "NotFound"


def test_simulate_unhandled_error(client):
    with pytest.raises(Exception):
        with app.app_context():
            client.get("/errors/simulate_unhandled_error")
