import pytest
from app import create_app
from app.extensions import db


@pytest.fixture
def client():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_register_login_me(client):
    r = client.post("/api/auth/register",
                    json={"name": "A", "email": "a@x.com", "password": "pw123"})
    assert r.status_code == 201

    r = client.post("/api/auth/login", json={"email": "a@x.com", "password": "pw123"})
    assert r.status_code == 200
    token = r.get_json()["data"]["token"]

    r = client.get("/api/users/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.get_json()["data"]["email"] == "a@x.com"


def test_bad_login(client):
    r = client.post("/api/auth/login", json={"email": "no@x.com", "password": "x"})
    assert r.status_code == 401
