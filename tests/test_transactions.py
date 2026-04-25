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

def test_create_transaction(client):
    token = get_token(client)

    category_response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "type": "expense"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    category_id = category_response.json()["id"]

    response = client.post(
        "/transactions/",
        json={
            "amount": "500.00",
            "type": "expense",
            "category_id": category_id,
            "description": "Lunch",
            "date": "2026-04-26"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201, response.json()

    data = response.json()

    assert data["amount"] == "500.00" or data["amount"] == 500.0
    assert data["type"] == "expense"
    assert data["category_id"] == category_id
    assert data["description"] == "Lunch"


def test_create_transaction_wrong_type(client):
    token = get_token(client)

    category_response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "type": "expense"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    category_id = category_response.json()["id"]

    response = client.post(
        "/transactions/",
        json={
            "amount": "500.00",
            "type": "income",
            "category_id": category_id,
            "description": "Wrong type",
            "date": "2026-04-26"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400

def test_get_transactions(client):
    token = get_token(client)

    category_response = client.post(
        "/categories/",
        json={
            "name": "Food",
            "type": "expense"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    category_id = category_response.json()["id"]

    client.post(
        "/transactions/",
        json={
            "amount": "500.00",
            "type": "expense",
            "category_id": category_id,
            "description": "Lunch",
            "date": "2026-04-26"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get(
        "/transactions/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["type"] == "expense"
    assert data[0]["category_id"] == category_id
    assert data[0]["description"] == "Lunch"