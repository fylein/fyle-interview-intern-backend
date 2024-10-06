import pytest
from flask import json
from core.apis.teachers.principal import principalteacher_blueprint
from core import create_app
from core.models.teachers import Teacher
from core.models.principals import Principal
from unittest.mock import patch

# Creating a new Flask app for testing
app = create_app()
app.register_blueprint(principalteacher_blueprint)

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_missing_x_principal(client):
    response = client.get('/principal/teachers')
    assert response.status_code == 400
    assert b"Missing X-Principal header" in response.data

def test_invalid_json_x_principal(client):
    response = client.get('/principal/teachers', headers={'X-Principal': 'invalid_json'})
    assert response.status_code == 400
    assert b"Invalid X-Principal header" in response.data

def test_missing_principal_id(client):
    response = client.get('/principal/teachers', headers={'X-Principal': json.dumps({})})
    assert response.status_code == 400
    assert b"Invalid X-Principal header" in response.data

def test_invalid_principal_id_type(client):
    response = client.get('/principal/teachers', headers={'X-Principal': json.dumps({'principal_id': 'string'})})
    assert response.status_code == 400
    assert b"Invalid principal_id" in response.data



def test_internal_server_error(client):
    pass  

def test_zero_principal_id(client):
    """
    Test principal_id as zero in the X-Principal header.
    """
    headers = {'X-Principal': json.dumps({'principal_id': 0})}
    response = client.get('/principal/teachers', headers=headers)
    assert response.status_code == 400
    assert b"Invalid principal_id" in response.data

def test_negative_principal_id(client):
    """
    Test principal_id as a negative number in the X-Principal header.
    """
    headers = {'X-Principal': json.dumps({'principal_id': -1})}
    response = client.get('/principal/teachers', headers=headers)
    assert response.status_code == 400
    assert b"Invalid principal_id" in response.data



def test_repr():
    principal = Principal(id=1)
    assert repr(principal) == '<Principal 1>'