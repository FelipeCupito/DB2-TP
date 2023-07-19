from fastapi import APIRouter, Depends
from backend.app.crud import users_dao
from backend.app.schemas import UserBase
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=UserBase)
def create_user(user: UserBase, db: Session = Depends(get_db)):
    return users_dao.create(user, db)


@router.get("/cbu/{cbu}", response_model=UserBase)
def read_user_by_cbu(cbu: str, db: Session = Depends(get_db)):
    return users_dao.get_by_cbu(cbu, db)


@router.get("/alias/{alias_type}", response_model=UserBase)
def read_user_by_alias(alias_type: str, db: Session = Depends(get_db)):
    return users_dao.get_by_alias(alias_type, db)
