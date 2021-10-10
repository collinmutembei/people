from jsf import JSF

from app.models.users import UserCreate


def test_docs(client):
    response = client.get(
        "/docs",
    )
    assert response.status_code == 200


def test_register_user(client):
    user = JSF(UserCreate.schema()).generate()
    response = client.post("/auth/register", json=user)
    assert response.ok
    assert response.status_code == 201
    assert not response.json()["is_verified"]
    assert response.json()["name"] == user["name"]
    assert response.json()["email"] == user["email"]


def test_login_jwt(client):
    user = JSF(UserCreate.schema()).generate()
    client.post(
        "/auth/register",
        json=user,
    )
    login_data = {"username": user["email"], "password": user["password"]}
    response = client.post(
        "/auth/jwt/login",
        data=login_data,
    )
    assert response.ok
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"
