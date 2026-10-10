
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestSession = sessionmaker(
        bind=test_engine,
        autoflush=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_vehicle(client):
    response = client.post(
        "/vehicles",
        json={
            "vehicle_id": "V101",
            "model": "Demo Sedan",
        },
    )

    assert response.status_code == 201
    assert response.json()["vehicle_id"] == "V101"


def test_duplicate_vehicle(client):
    payload = {
        "vehicle_id": "V101",
        "model": "Demo Sedan",
    }

    client.post("/vehicles", json=payload)
    response = client.post("/vehicles", json=payload)

    assert response.status_code == 409


def test_unknown_vehicle(client):
    response = client.post(
        "/telemetry",
        json={
            "vehicle_id": "UNKNOWN",
            "speed": 60,
            "engine_temperature": 90,
            "fuel_level": 75,
        },
    )

    assert response.status_code == 404


def test_high_temperature_creates_alert(client):
    client.post(
        "/vehicles",
        json={
            "vehicle_id": "V101",
            "model": "Demo Sedan",
        },
    )

    response = client.post(
        "/telemetry",
        json={
            "vehicle_id": "V101",
            "speed": 40,
            "engine_temperature": 130,
            "fuel_level": 65,
        },
    )

    assert response.status_code == 201

    alerts = client.get("/alerts?vehicle_id=V101")

    assert alerts.status_code == 200
    assert len(alerts.json()) == 1
    assert (
        alerts.json()[0]["alert_type"]
        == "HIGH_ENGINE_TEMPERATURE"
    )


def test_invalid_fuel_level(client):
    client.post(
        "/vehicles",
        json={
            "vehicle_id": "V101",
            "model": "Demo Sedan",
        },
    )

    response = client.post(
        "/telemetry",
        json={
            "vehicle_id": "V101",
            "speed": 60,
            "engine_temperature": 90,
            "fuel_level": 150,
        },
    )

    assert response.status_code == 422
