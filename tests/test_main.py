import pytest
from fastapi.testclient import TestClient
from app.main import app, tron_client
from app.database import SessionLocal, engine
from app.models import Base, Request
from app.dependencies import get_db

@pytest.fixture
def test_client():
    """Фикстура для тестирования"""
    return TestClient(app)

@pytest.fixture
def test_db():
    """Фикстура для тестовой базы данных"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_get_address_info(test_client, test_db, monkeypatch):
    """Интеграционный тест для эндпоинта /address/"""
    def mock_get_balance(address):
        return 150.5
    
    def mock_get_resources(address):
        return {"freeNetLimit": 1000, "EnergyLimit": 5000}
    
    monkeypatch.setattr(tron_client, "get_balance", mock_get_balance)
    monkeypatch.setattr(tron_client, "get_resources", mock_get_resources)

    app.dependency_overrides[get_db] = lambda: test_db

    response = test_client.post("/address/", json={"address": "TEST123"})

    assert response.status_code == 200
    assert response.json() == {
        "address": "TEST123",
        "balance": 150.5,
        "bandwidth": 1000,
        "energy": 5000
    }

    db_record = test_db.query(Request).first()
    assert db_record.address == "TEST123"
    