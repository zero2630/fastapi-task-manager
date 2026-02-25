import pytest


@pytest.mark.anyio
@pytest.mark.parametrize(
    "title,description",
    [
        ("Task1", None),
        ("Task1", ""),
        ("Task1", "description of task"),
    ],
)
async def test_create_task(client, user_token, title, description):
    headers = {"Authorization": f"Bearer {user_token}"}
    body = {
        "title": title,
    }
    if description is not None:
        body.update({"description": description})

    response = await client.post(
        "/tasks",
        headers=headers,
        json=body,
    )
    response_data = response.json()

    assert response.status_code == 200
    assert "title" in response_data
    assert "description" in response_data
    assert response_data["title"] == title
    assert response_data["description"] == description or (
        description is None and response_data["description"] == ""
    )


@pytest.mark.anyio
async def test_create_task_unauthorized(client, user_token):
    body = {"title": "Task1"}

    response = await client.post("/tasks", json=body)

    assert response.status_code == 401


@pytest.mark.anyio
@pytest.mark.parametrize("title", ["Task2", None])
@pytest.mark.parametrize("description", ["updated description", None])
async def test_update_task(client, user_token, title, description):
    if title is None and description is None:
        pytest.skip("all None")

    headers = {"Authorization": f"Bearer {user_token}"}
    body = {"title": "Task1"}

    response = await client.post(
        "/tasks",
        headers=headers,
        json=body,
    )

    assert response.status_code == 200

    task_id = response.json()["id"]

    body = {}

    if title is not None:
        body.update({"title": title})
    if description is not None:
        body.update({"description": description})

    response = await client.patch(
        f"/tasks/{task_id}",
        headers=headers,
        json=body,
    )
    response_data = response.json()

    assert response.status_code == 200
    assert "title" in response_data
    assert "description" in response_data
    if title is not None:
        assert response_data["title"] == title
    if description is not None:
        assert response_data["description"] == description
