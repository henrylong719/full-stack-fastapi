from tests.utils import get_auth_headers


def test_read_items_as_admin_sees_all_seed_items(client):
    headers = get_auth_headers(client, "admin@example.com", "changethis123")
    response = client.get("/api/v1/items/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 3  # seeded items
    assert len(data["data"]) >= 3


def test_read_items_as_alice_sees_only_own_items(client):
    headers = get_auth_headers(client, "alice@example.com", "password123")
    response = client.get("/api/v1/items/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 2
    # Alice should not see admin's seed item title
    titles = [item["title"] for item in data["data"]]
    assert "Admin Test Item" not in titles


def test_create_item_and_read_it_as_owner(client):
    headers = get_auth_headers(client, "alice@example.com", "password123")

    create_res = client.post(
        "/api/v1/items/",
        headers=headers,
        json={"title": "Lantern", "description": "LED camping lantern"},
    )
    assert create_res.status_code == 201, create_res.text
    created = create_res.json()
    item_id = created["id"]
    assert created["title"] == "Lantern"

    read_res = client.get(f"/api/v1/items/{item_id}", headers=headers)
    assert read_res.status_code == 200
    assert read_res.json()["title"] == "Lantern"


def test_alice_cannot_access_admin_item(client):
    admin_headers = get_auth_headers(client, "admin@example.com", "changethis123")
    alice_headers = get_auth_headers(client, "alice@example.com", "password123")

    admin_items_res = client.get("/api/v1/items/", headers=admin_headers)
    assert admin_items_res.status_code == 200
    admin_items = admin_items_res.json()["data"]

    # Find admin-owned seed item
    admin_item = next(
        item for item in admin_items if item["title"] == "Admin Test Item"
    )
    admin_item_id = admin_item["id"]

    read_res = client.get(f"/api/v1/items/{admin_item_id}", headers=alice_headers)
    assert read_res.status_code == 403


def test_owner_can_update_and_delete_item(client):
    headers = get_auth_headers(client, "alice@example.com", "password123")

    create_res = client.post(
        "/api/v1/items/",
        headers=headers,
        json={"title": "Sleeping Bag", "description": "Warm and light"},
    )
    assert create_res.status_code == 201
    item_id = create_res.json()["id"]

    patch_res = client.patch(
        f"/api/v1/items/{item_id}",
        headers=headers,
        json={"title": "Sleeping Bag Pro"},
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["title"] == "Sleeping Bag Pro"

    delete_res = client.delete(f"/api/v1/items/{item_id}", headers=headers)
    assert delete_res.status_code == 200
    assert delete_res.json()["message"] == "Item deleted successfully"

    read_deleted = client.get(f"/api/v1/items/{item_id}", headers=headers)
    assert read_deleted.status_code == 404
