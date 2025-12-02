
def test_protected_routes_without_token(client):
    protected = [
        ("GET", "/api/carrinhos"),
        ("POST", "/api/carrinhos", {"name": "Cart Test"}),
    ]
    for method, path, *rest in protected:
        if method == "GET":
            resp = client.get(path)
        else:
            data = rest[0] if rest else {}
            resp = client.post(path, json=data)
        assert resp.status_code in (401, 422)  # 401 se sem token, 422 se payload inválido
