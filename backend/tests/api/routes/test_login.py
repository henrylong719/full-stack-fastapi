from tests.utils import get_auth_headers


def test_login_access_token_success_admin(client):
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": "admin@example.com", "password": "changethis123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "access_token" in response.cookies
    assert "csrf_token" in response.cookies


def test_login_access_token_success_alice(client):
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": "alice@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_access_token_wrong_password(client):
    response = client.post(
        "/api/v1/login/access-token",
        data={"username": "alice@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_test_token_requires_auth(client):
    response = client.post("/api/v1/login/test-token")
    assert response.status_code in (401, 403)  # FastAPI auth layer may return 401


def test_test_token_returns_current_user(client):
    headers = get_auth_headers(client, "alice@example.com", "password123")
    response = client.post("/api/v1/login/test-token", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["is_superuser"] is False


def test_cookie_auth_requires_csrf_for_unsafe_methods(client):
    login_res = client.post(
        "/api/v1/login/access-token",
        data={"username": "alice@example.com", "password": "password123"},
    )
    assert login_res.status_code == 200

    me_res = client.get("/api/v1/users/me")
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "alice@example.com"

    missing_csrf_res = client.patch(
        "/api/v1/users/me",
        json={"full_name": "Alice Missing CSRF"},
    )
    assert missing_csrf_res.status_code == 403

    csrf_token = login_res.cookies["csrf_token"]
    valid_csrf_res = client.patch(
        "/api/v1/users/me",
        headers={"X-CSRF-Token": csrf_token},
        json={"full_name": "Alice CSRF"},
    )
    assert valid_csrf_res.status_code == 200
    assert valid_csrf_res.json()["full_name"] == "Alice CSRF"


def test_login_rate_limit_after_repeated_failures(client):
    for _ in range(5):
        response = client.post(
            "/api/v1/login/access-token",
            data={"username": "ratelimit@example.com", "password": "wrongpassword"},
        )
        assert response.status_code == 400

    blocked = client.post(
        "/api/v1/login/access-token",
        data={"username": "ratelimit@example.com", "password": "wrongpassword"},
    )
    assert blocked.status_code == 429
