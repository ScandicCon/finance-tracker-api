def get_token(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "test@example.com",
            "password": "password123"
        }
    )

    return response.json()["access_token"]


def test_create_category(client):
    token = get_token(client)

    response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "type": "expense"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print(response.status_code)
    print(response.json())
    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Food"
    assert data["type"] == "expense"
    assert "id" in data
def test_get_categories(client):
    token = get_token(client)

    client.post(
        "/categories/",
        json={
            "name": "Food",
            "type": "expense"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get(
        "/categories/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Food"
    assert data[0]["type"] == "expense"