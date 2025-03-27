from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AddressRequest(BaseModel):
    """Схема для входных данных - только адрес."""
    address: str

class AddressResponse(BaseModel):
    """Схема для ответа с данными об адресе."""
    address: str
    balance: float
    bandwidth: int
    energy: int

class RequestHistory(BaseModel):
    """Схема для истории запросов."""
    id: int
    address: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
    