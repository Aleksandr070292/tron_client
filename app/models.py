from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime, UTC

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(UTC))

    def __repr__(self):
        return f"<Request(address='{self.address}', timestamp='{self.timestamp}')>"