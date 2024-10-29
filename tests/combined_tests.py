from core.libs.exceptions import FyleError

def test_non_existent_route_access(client):
    result = client.get('/inexistent')
    assert result.status_code == 404
    assert result.json['error'] == 'NotFound'

def test_fyle_error_handling():
    msg = "Test FyleError message"
    code = 400
    custom_error = FyleError(code, msg)
    error_data = custom_error.to_dict()
    assert isinstance(error_data, dict)
    assert error_data['message'] == msg