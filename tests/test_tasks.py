import pytest

@pytest.fixture
def create_user_and_auth(client):
    def _create_user_and_auth(email="u1@example.com", name="U1", password="testpass123"):
        res = client.post("/auth/register", json={"email": email, "name": name, "password": password})
        assert res.status_code == 201

        token_res = client.post("/auth/token", data={"username": email, "password": password})
        assert token_res.status_code == 200
        token = token_res.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return _create_user_and_auth


def test_create_and_list_tasks(client, create_user_and_auth):
    auth_headers = create_user_and_auth(email="u1@example.com", name="U1")

    t1 = client.post("/tasks/me", headers=auth_headers, json={"title": "Write README"})
    assert t1.status_code == 201

    t2 = client.post("/tasks/me", headers=auth_headers, json={"title": "Add tests"})
    assert t2.status_code == 201

    # List tasks
    r = client.get("/tasks/me", headers=auth_headers)
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2
    assert set([i["title"] for i in items]) == {"Write README", "Add tests"}


def test_task_update_and_filter(client, create_user_and_auth):
    auth_headers = create_user_and_auth(email="u2@example.com", name="U2")

    t = client.post("/tasks/me", headers=auth_headers, json={"title": "Do chores"})
    assert t.status_code == 201
    tid = t.json()["id"]

    r_upd = client.patch(f"/tasks/{tid}", headers=auth_headers, json={"done": True})
    assert r_upd.status_code == 200
    assert r_upd.json()["done"] is True

    r_done = client.get("/tasks/me?done=true", headers=auth_headers)
    assert r_done.status_code == 200
    items = r_done.json()
    assert len(items) == 1
    assert items[0]["id"] == tid


def test_delete_task(client, create_user_and_auth):
    auth_headers = create_user_and_auth(email="u3@example.com", name="U3")

    t = client.post("/tasks/me", headers=auth_headers, json={"title": "Temp"})
    assert t.status_code == 201
    tid = t.json()["id"]

    r_del = client.delete(f"/tasks/{tid}", headers=auth_headers)
    assert r_del.status_code == 204

    r_del2 = client.delete(f"/tasks/{tid}", headers=auth_headers)
    assert r_del2.status_code == 404
