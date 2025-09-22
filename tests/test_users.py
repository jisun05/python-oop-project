# tests/test_users.py
def test_create_user(client):
    payload = {"email": "alice@example.com", "name": "Alice"}
    r = client.post("/users", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["id"] > 0
    assert data["email"] == payload["email"]
    assert data["name"] == payload["name"]

def test_create_user_duplicate_email(client):
    payload = {"email": "dup@example.com", "name": "Dup"}
    r1 = client.post("/users", json=payload)
    assert r1.status_code == 201
    r2 = client.post("/users", json=payload)
    assert r2.status_code == 400
    assert r2.json()["detail"].lower().find("already") >= 0

def test_get_user_by_id(client):
    # 먼저 생성
    created = client.post("/users", json={"email": "bob@example.com", "name": "Bob"}).json()
    uid = created["id"]

    r = client.get(f"/users/{uid}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == uid
    assert data["email"] == "bob@example.com"
