def test_api_health(client):
    response = client.get(
        "/healthz/",
    )
    assert response.status_code == 200
    assert response.json() == {}
