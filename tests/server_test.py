def test_base_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    status = response.json["status"]
    assert status == "ready"


def test_invalid_endpoint(client, h_principal):
    response = client.get("/invalid_endpoint", headers=h_principal)
    assert response.status_code == 404