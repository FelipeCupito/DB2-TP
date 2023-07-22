from fastapi import APIRouter
from backend.app.crud import users_dao, banks_dao

from backend.app.models import User
from backend.app.routers.utils import _send_data, _send_error
from backend.app.schemas import Response

router = APIRouter()


@router.post("/", response_model=Response)
def create_user(user: User):
    if users_dao.check_cbu_exist(user):
        return _send_error("CBU already exists")
    if users_dao.check_alias_exist(user.alias):
        return _send_error("Alias already exists")
    if not banks_dao.check_bank_exist(user.bank_id):
        return _send_error("Bank does not exist")

    user = users_dao.create(user)
    return _send_data(user)


@router.get("/cbu/{cbu}", response_model=Response)
def read_user_by_cbu(cbu: str):
    user = users_dao.get_by_cbu(cbu)
    if user is None:
        return _send_error("User not found")
    return _send_data(user)


@router.get("/alias/{alias_type}", response_model=Response)
def read_user_by_alias(alias: str):
    user = users_dao.get_by_alias(alias)
    if user is None:
        return _send_error("User not found")
    return _send_data(user)


