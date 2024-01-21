
def test_base_endpoint(client):
    response = client.get(
        '/'
    )

    assert response.status_code == 200

    status = response.json['status']
    assert status == "ready"

def test_invalid_endpoint(client, h_principal):
    """
    failure case: If invalid url is being triggered
    """
    response = client.get(
        '/invalid',
        headers=h_principal
    )

    assert response.status_code == 404