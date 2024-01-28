# Change : Test cases for server testing

def test_app_ready(client, h_student_1):
    """Test app.route('/')"""
    response = client.get(
        '/',
        headers=h_student_1
    )

    assert response.status_code == 200

def test_http_error(client, h_student_1):
    """Test Http Error . Non-Existent Page"""
    response = client.get(
        '/aaaa',
        headers=h_student_1
    )

    assert response.status_code == 404





