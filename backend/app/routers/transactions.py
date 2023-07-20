from fastapi import APIRouter, Depends
from backend.app.crud import transactions_dao
from backend.app.schemas import Transaction
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.post("/pay-cbu", response_model=Transaction)
def pay_by_cbu(from_cbu: str, to_cbu: str, amount: float, db: Session = Depends(get_db)):
    return transactions_dao.pay_by_cbu(from_cbu, to_cbu, amount, db)


@router.post("/pay-alias", response_model=Transaction)
def pay_by_cbu(from_alias: str, to_alias: str, amount: float, db: Session = Depends(get_db)):
    return transactions_dao.pay_by_alias(from_alias, to_alias, amount, db)
