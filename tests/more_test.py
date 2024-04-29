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


def test_fyle_error_creation():
    """
    Test to check that FyleError handling is working properly.
    """
    error_message = "Test FyleError message"
    error_code = 400

    fyle_error = FyleError(error_code, error_message)

    assert fyle_error.status_code == error_code
    assert fyle_error.message == error_message


def test_fyle_error_to_dict():
    """
    Test to check that FyleError handling is working properly. 
    """
    error_message = "Test FyleError message"
    error_code = 400

    fyle_error = FyleError(error_code, error_message)
    error_dict = fyle_error.to_dict()

    assert isinstance(error_dict, dict)
    assert error_dict['message'] == error_message