from fastapi import APIRouter
from backend.app.crud import users_dao
from backend.app.schemas import UserBase

router = APIRouter()

@router.post("/", response_model=UserBase)
def create_user(user: UserBase):
    return users_dao.create(user)


@router.get("/cbu/{cbu}", response_model=UserBase)
def read_user_by_cbu(cbu: str):
    return users_dao.get_by_cbu(cbu)


@router.get("/alias/{alias_type}", response_model=UserBase)
def read_user_by_alias(alias_type: str):
    return users_dao.get_by_alias(alias_type)
