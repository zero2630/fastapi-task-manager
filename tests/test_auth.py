import pytest


@pytest.mark.anyio
async def test_signup(client):
    body = {
        "email": "kekw@example.com",
        "password": "12345678",
    }

    response = await client.post("/signup", json=body)
    data = response.json()

    assert response.status_code == 200
    assert "email" in data
    assert "id" in data
    assert "created_at" in data


@pytest.mark.anyio
async def test_signup_conflict(client, test_user):
    body = {
        "email": "kekw@example.com",
        "password": "12345678",
    }

    response = await client.post("/signup", json=body)

    assert response.status_code == 409


@pytest.mark.anyio
async def test_token(client, test_user):
    data = {
        "username": "kekw@example.com",
        "password": "12345678",
    }

    response = await client.post("/token", data=data)
    response_data = response.json()

    assert response.status_code == 200
    assert "access_token" in response_data
    assert "token_type" in response_data
    assert response_data["token_type"] == "bearer"


@pytest.mark.anyio
async def test_token_unauthorized(client, test_user):
    data = {
        "username": "kekw@example.com",
        "password": "11111111",
    }

    response = await client.post("/token", data=data)

    assert response.status_code == 401


@pytest.mark.anyio
async def test_user_info(client, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}

    response = await client.get("/users/me", headers=headers)
    response_data = response.json()
    assert response.status_code == 200
    assert "email" in response_data
    assert "id" in response_data
    assert "created_at" in response_data
    assert response_data["email"] == "kekw@example.com"


@pytest.mark.anyio
async def test_user_info_fail(client):
    response = await client.get("/users/me")
    assert response.status_code == 401
