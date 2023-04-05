def test_auth_assertion(client):
    response = client.get(
        '/student/assignments',
    )

    error_response = response.json
    assert response.status_code == 401
    assert error_response['error'] == 'FyleError' 
    assert error_response["message"] == 'principal not found'

def test_access_assertion(client, h_teacher_1):
    response = client.get(
        '/student/assignments',
        headers = h_teacher_1
    )

    error_response = response.json
    assert response.status_code == 403
    assert error_response['error'] == 'FyleError' 
    assert error_response["message"] == 'requester should be a student'

