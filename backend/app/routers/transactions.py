from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.crud import transactions_dao
from ..database import get_db
from ..schemas import UserBase

router = APIRouter()


@router.post("/{cbu}/pay", response_model=float)
def pay(cbu: str, amount: float, db: Session = Depends(get_db)):
    return transactions_dao.pay(cbu, amount, db)


@router.post("/{cbu}/charge", response_model=float)
def charge(cbu: str, amount: float, db: Session = Depends(get_db)):
    return transactions_dao.charge(cbu, amount, db)
