from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backendBanks.app.crud import transactions_dao
from ..database import get_db

router = APIRouter()


@router.post("/{cbu}/pay", response_model=float)
def pay(cbu: str, amount: float, db: Session = Depends(get_db)):
    try:
        balance = transactions_dao.pay(cbu, amount, db)
        if balance == -1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        elif balance == -2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")
        else:
            return balance
    except HTTPException:
        raise

@router.post("/{cbu}/charge", response_model=float)
def charge(cbu: str, amount: float, db: Session = Depends(get_db)):
    try:
        balance = transactions_dao.charge(cbu, amount, db)
        if balance == -1:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        else:
            return balance
    except HTTPException:
        raise