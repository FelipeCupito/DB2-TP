from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import ResponseValidationError

from backendBanks.app.crud import users_dao
from backendBanks.app.schemas import UserBase
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.get("/{cbu}", response_model=UserBase)
def get_user_info(cbu: str, db: Session = Depends(get_db)):
    try:
        user = users_dao.get_info(cbu, db)
        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except HTTPException:
        raise
    except ResponseValidationError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Account information wrongly formatted")


@router.get("/{cbu}/balance", response_model=float)
def get_user_balance(cbu: str, db: Session = Depends(get_db)):
    try:
        balance = users_dao.get_balance(cbu, db)
        if balance:
            return balance
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    except HTTPException:
        raise
    except ResponseValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account information wrongly formatted")
