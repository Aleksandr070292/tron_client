from sqlalchemy.orm import Session
from .database import SessionLocal

def get_db():
    """Получение сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        