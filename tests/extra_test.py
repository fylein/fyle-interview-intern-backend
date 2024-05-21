from core.libs.exceptions import FyleError


def test_root_endpoint(client):
    """
    Test to check server is running correctly.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'ready'


def test_error_handling_validation_error(client, h_teacher_1):
    """
    Test to check validation error handling
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={})
    assert response.status_code == 400
    assert response.json['error'] == 'ValidationError'


def test_error_handling_http_exception(client):
    """
    failure case: When an invalid endpoint is requested
    """
    response = client.get('/nonexistent-route')
    assert response.status_code == 404
    assert response.json['error'] == 'NotFound'


