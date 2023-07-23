from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import ResponseValidationError

from backend.app.crud import users_dao
from backend.app.schemas import UserBase
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.get("/{cbu}", response_model=UserBase)
def get_user_info(cbu: str, db: Session = Depends(get_db)):
    return users_dao.get_info(cbu, db)
    # try:
    #     user = users_dao.get_info(cbu, db)
    # except ValueError:
    #     raise Exception("User information incorrectly formatted.")
    # return user



@router.get("/{cbu}/balance", response_model=float)
def get_user_balance(cbu: str, db: Session = Depends(get_db)):
    return users_dao.get_balance(cbu, db)
