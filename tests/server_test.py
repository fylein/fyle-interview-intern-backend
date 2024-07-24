# This test the server is ready or not 
def test_server_health(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json['status'] == 'ready'