from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, engine, SessionLocal
from app.core.config import get_settings

client = TestClient(app)


def setup_module():
    Base.metadata.create_all(bind=engine)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200


def test_register_and_login():
    r = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "secret123",
        "full_name": "Test User",
    })
    assert r.status_code in (201, 400)  # 400 if already exists

    r = client.post("/api/v1/auth/login?email=test@example.com&password=secret123")
    assert r.status_code == 200
    assert "access_token" in r.json()
