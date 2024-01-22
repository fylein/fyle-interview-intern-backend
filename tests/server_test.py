def test_base_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200

    status = response.json["status"]
    assert status == "ready"


def test_invalid_endpoint(client, h_principal):
    """
    failure case: If an invalid endpoint is hit
    """
    response = client.get("/invalid", headers=h_principal)

    assert response.status_code == 404
