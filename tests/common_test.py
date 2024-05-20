from core.libs.exceptions import FyleError

def test_hitting_non_existent_route(client):
    response = client.get('/inexistent')
    assert response.status_code == 404
    assert response.json['error'] == 'NotFound'

def test_fyle():
    error_message = "Test FyleError message"
    error_code = 400
    fyle_error = FyleError(error_code, error_message)
    error_dict = fyle_error.to_dict()
    assert isinstance(error_dict, dict)
    assert error_dict['message'] == error_message