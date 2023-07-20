from fastapi import APIRouter, Depends
from backend.app.crud import banks_dao
from backend.app.schemas import Bank
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=Bank)
def create_bank(bank: Bank, db: Session = Depends(get_db)):
    return banks_dao.create(bank, db)
