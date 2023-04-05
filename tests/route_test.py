def test_api_not_exist(client):
    response = client.get(
        '/students',
      
    )

    assert response.status_code == 404

    data = response.json
    assert data['error'] == "NotFound"
    assert data['message'] == "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."

   
