def test_register_and_login_success(client):
    # Registro
    resp = client.post("/api/register", json={"username": "testuser", "password": "password123"})
    assert resp.status_code == 200
    body = resp.json()
    assert "message" in body and "sucesso" in body["message"].lower()

    # Login
    resp = client.post("/api/login", json={"username": "testuser", "password": "password123"})
    assert resp.status_code == 200
    body = resp.json()
    assert "access_token" in body
    assert body.get("token_type") == "bearer"

def test_register_duplicate_username(client):
    # Primeiro registro
    resp = client.post("/api/register", json={"username": "dupuser", "password": "pwd"})
    assert resp.status_code == 200

    # Segundo registro com mesmo username
    resp = client.post("/api/register", json={"username": "dupuser", "password": "outrapwd"})
    assert resp.status_code == 400
