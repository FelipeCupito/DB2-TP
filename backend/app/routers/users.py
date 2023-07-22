from fastapi import APIRouter, Depends
from backend.app.crud import users_dao
from backend.app.schemas import UserBase
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.get("/{cbu}", response_model=UserBase)
def get_user_info(cbu: str, db: Session = Depends(get_db)):
    return users_dao.get_info(cbu, db)


@router.get("/{cbu}/balance", response_model=float)
def get_user_balance(cbu: str, db: Session = Depends(get_db)):
    return users_dao.get_balance(cbu, db)
