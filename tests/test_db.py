import pytest
from sqlalchemy.orm import Session
from app.models import Request
from app.database import SessionLocal, engine, Base
from datetime import datetime

@pytest.fixture
def test_db():
    """Фикстура для тестовой базы данных"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_db_write(test_db: Session):
    """Тест записи в базу данных"""
    new_request = Request(address="TEST456")
    test_db.add(new_request)
    test_db.commit()

    saved_request = test_db.query(Request).filter_by(address="TEST456").first()
    assert saved_request is not None
    assert saved_request.address == "TEST456"
    assert isinstance(saved_request.timestamp, datetime)
     