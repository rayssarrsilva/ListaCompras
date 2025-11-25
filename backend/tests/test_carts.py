import pytest
from fastapi import status

def test_login_for_access_token(client, test_user):
    """Testa login e obtenção de token JWT."""
    response = client.post(
        "/api/login",
        json={"username": test_user["username"], "password": test_user["password"]}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_cart_unauthorized(client):
    """Tenta criar carrinho sem autenticação → deve falhar."""
    response = client.post("/api/carrinhos", json={"name": "Test Cart"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_and_list_carts(client, test_user):
    """Testa fluxo completo: login → criar carrinho → listar carrinhos."""
    # 1. Login
    login_response = client.post(
        "/api/login",
        json={"username": test_user["username"], "password": test_user["password"]}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Criar carrinho
    cart_response = client.post(
        "/api/carrinhos",
        json={"name": "Minha Lista"},
        headers=headers
    )
    assert cart_response.status_code == status.HTTP_200_OK
    cart_id = cart_response.json()["id"]

    # 3. Listar carrinhos
    list_response = client.get("/api/carrinhos", headers=headers)
    assert list_response.status_code == status.HTTP_200_OK
    carts = list_response.json()
    assert len(carts) >= 1
    assert any(cart["id"] == cart_id for cart in carts)

def test_get_cart_items_unauthorized(client):
    """Tenta acessar itens de carrinho sem token → falha."""
    response = client.get("/api/carrinhos/1/itens")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED