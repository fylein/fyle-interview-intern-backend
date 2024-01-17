def test_get_ready(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json['status'] == 'ready'
    assert response.json['time'] is not None