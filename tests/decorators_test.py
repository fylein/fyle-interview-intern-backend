
def test_unauthorized_exception(client):
    """
    failure case: If X-Principal header is not present
    """
    response = client.get(
        '/student/assignments',
    )

    assert response.status_code == 401


def test_forbidden_exception(client, h_invalid_header):
    """
    failure case: If user is not allowed to use triggered api
    """
    response = client.get(
        '/principal/teachers',
        headers=h_invalid_header
    )

    assert response.status_code == 403