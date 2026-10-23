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

def test_vr_flow_create_account_otp_face_login(client):
    # 1. CREATE ACCOUNT - As per your paper Point 1
    r = client.post("/api/auth/create-account",
                    json={"name": "VR User", "email": "vr@test.com", "password": "vr123456"})
    assert r.status_code == 200
    data = r.get_json()
    assert data["success"] == True
    otp = data["otp"]  # Get OTP from response
    print(f"OTP is: {otp}")

    # 2. VERIFY OTP - Field 3
    r = client.post("/api/auth/verify-otp", 
                    json={"email": "vr@test.com", "otp_code": otp})
    assert r.status_code == 200
    assert r.get_json()["success"] == True

    # 3. FACE VERIFICATION - Field 4
    r = client.post("/api/auth/face-verification",
                    json={"email": "vr@test.com"})
    assert r.status_code == 200
    assert r.get_json()["success"] == True

    # 4. LOGIN - Point 2
    r = client.post("/api/auth/login", 
                    json={"email": "vr@test.com", "password": "vr123456"})
    assert r.status_code == 200
    json_data = r.get_json()
    assert json_data["status"] == "valid"
    assert json_data["message"] == "Open APP"

    # 5. CLAIM COINS - Field 5
    r = client.post("/api/auth/claim-coins",
                    json={"email": "vr@test.com", "coins": 100})
    assert r.status_code == 200
    assert r.get_json()["total_coins"] == 100

    # 6. BONUS COINS - Field 7
    r = client.post("/api/auth/refer-bonus",
                    json={"email": "vr@test.com"})
    assert r.status_code == 200
    assert r.get_json()["total_coins"] == 150  # 100 + 50 bonus

def test_bad_login_invalid_password(client):
    # Create user first
    client.post("/api/auth/create-account",
                json={"name": "A", "email": "a@x.com", "password": "pw123456"})
    
    r = client.post("/api/auth/login", json={"email": "a@x.com", "password": "wrongpass"})
    assert r.status_code == 401
    assert r.get_json()["status"] == "Invalid"

def test_bad_otp(client):
    client.post("/api/auth/create-account",
                json={"name": "B", "email": "b@x.com", "password": "pw123456"})
    
    r = client.post("/api/auth/verify-otp",
                    json={"email": "b@x.com", "otp_code": "000000"})
    assert r.status_code == 400
