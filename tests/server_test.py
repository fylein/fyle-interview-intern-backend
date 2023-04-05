def test_server(client):
    res = client.get(
        '/'
    )
    response = res.json
    assert response["status"] == "ready"

def test_server_error_handler_http(client):
    res = client.post(
        '/'
    )

    error_response = res.json

    assert error_response["error"] == "MethodNotAllowed"
    assert error_response["message"] == "405 Method Not Allowed: The method is not allowed for the requested URL."
