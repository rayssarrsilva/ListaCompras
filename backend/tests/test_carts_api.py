import pytest

def perform_auth_and_get_token(client):
    # cria usuário
    client.post("/api/register", json={"username": "cartuser", "password": "senha"})
    resp = client.post("/api/login", json={"username": "cartuser", "password": "senha"})
    return resp.json()["access_token"]

@pytest.fixture()
def auth_headers(client):
    token = perform_auth_and_get_token(client)
    return {"Authorization": f"Bearer {token}"}

def test_create_and_list_cart(client, auth_headers):
    # Cria carrinho
    resp = client.post("/api/carrinhos", json={"name": "Carrinho 1"}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data and data["name"] == "Carrinho 1"

    # Lista carrinhos
    resp = client.get("/api/carrinhos", headers=auth_headers)
    assert resp.status_code == 200
    carts = resp.json()
    assert any(c["name"] == "Carrinho 1" for c in carts)

def test_add_item_and_list_items(client, auth_headers):
    # Cria carrinho
    resp = client.post("/api/carrinhos", json={"name": "Cart para itens"}, headers=auth_headers)
    cart_id = resp.json()["id"]

    # Adiciona item
    resp = client.post(f"/api/carrinhos/{cart_id}/itens", json={"name": "Banana"}, headers=auth_headers)
    assert resp.status_code == 200
    item = resp.json()
    assert "id" in item and item["name"] == "Banana"

    # Lista itens
    resp = client.get(f"/api/carrinhos/{cart_id}/itens", headers=auth_headers)
    assert resp.status_code == 200
    items = resp.json()
    assert any(i["name"] == "Banana" for i in items)
