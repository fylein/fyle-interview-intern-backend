def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "ready"


def test_invalid_endpoint(client, h_principal):
    response = client.get("/other", headers=h_principal)
    assert response.status_code == 404
    assert response.json["error"] == "NotFound"

def test_non_existent_resource(client, h_principal):
    response = client.get("/non-existent", headers=h_principal)
    assert response.status_code == 404
    assert response.json["error"] == "NotFound"
def test_unauthorized_access(client):
    response = client.get("/principal/assignments")
    assert response.status_code == 401
    assert response.json["error"] == "FyleError"
def test_incorrect_method(client, h_principal):
    response = client.post("/principal/assignments", headers=h_principal)
    assert response.status_code == 405
    assert response.json["error"] == "MethodNotAllowed"