# Feature: Test when hitting base url


def test_base_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    status = response.json["status"]
    assert status == "ready"


# Feature: Test in case of hitting invalid endpoint


def test_invalid_endpoint(client, h_principal):
    response = client.get("/invalid", headers=h_principal)
    assert response.status_code == 404