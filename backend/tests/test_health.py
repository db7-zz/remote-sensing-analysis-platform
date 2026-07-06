def test_health_check_remains_available(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.get_json()["data"]["status"] == "healthy"

