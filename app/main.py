import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import AddressRequest, AddressResponse, RequestHistory
from .dependencies import get_db
from .tron_client import TronClient
from .models import Request
from .database import init_db
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Tron Address Info Service")
tron_client = TronClient()

init_db()
logger.debug("База данных инициализирована")

def validate_tron_address(address: str) -> bool:
    """Проверяет, является ли строка валидным Tron-адресом."""
    pattern = r'^T[a-zA-Z0-9]{33}$'
    return bool(re.match(pattern, address))

@app.post("/address/", response_model=AddressResponse)
async def get_address_info(request: AddressRequest, db: Session = Depends(get_db)):
    logger.debug(f"Получен запрос для адреса: {request.address}")
    
    if not validate_tron_address(request.address):
        raise HTTPException(status_code=400, detail="Невалидный Tron-адрес")
    
    try:
        balance = tron_client.get_balance(request.address)
        logger.debug(f"Баланс: {balance}")
        resources = tron_client.get_resources(request.address)
        logger.debug(f"Ресурсы: {resources}")
        
        bandwidth = resources.get("freeNetLimit", 0)  
        energy = resources.get("EnergyLimit", 0)  

        db_request = Request(address=request.address)
        logger.debug("Создан объект Request")
        db.add(db_request)
        logger.debug("Добавлен в сессию")
        db.commit()
        logger.debug("Коммит выполнен")

        response = AddressResponse(
            address=request.address,
            balance=balance,
            bandwidth=bandwidth,
            energy=energy
        )
        logger.debug(f"Ответ сформирован: {response}")
        return response
    
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при запросе данных: {str(e)}")

@app.get("/history/", response_model=list[RequestHistory])
async def get_request_history(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    logger.debug(f"Запрос истории: skip={skip}, limit={limit}")
    try:
        history = db.query(Request).order_by(Request.timestamp.desc()).offset(skip).limit(limit).all()
        logger.debug(f"Найдено записей: {len(history)}")
        return history
    except Exception as e:
        logger.error(f"Ошибка при получении истории: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ошибка при получении истории: {str(e)}")