from fastapi import APIRouter
from backendPixie.app.crud import users_dao, banks_dao

from backendPixie.app.models import User
from backendPixie.app.routers.utils import send_data, send_error
from backendPixie.app.schemas import Response

router = APIRouter()


@router.post("/", response_model=Response)
def create_user(user: User):
    if users_dao.check_cbu_exist(user.cbu):
        return send_error("CBU already exists")
    if users_dao.check_alias_exist(user.alias):
        return send_error("Alias already exists")
    if not banks_dao.check_bank_exist(user.bank_port):
        return send_error("Bank does not exist")

    user = users_dao.create(user)
    return send_data(user)


@router.get("/cbu/{cbu}", response_model=Response)
def read_user_by_cbu(cbu: str):
    user = users_dao.get_by_cbu(cbu)
    if user is None:
        return send_error("User not found")
    return send_data(user)


@router.get("/alias/{alias_type}", response_model=Response)
def read_user_by_alias(alias: str):
    user = users_dao.get_by_alias(alias)
    if user is None:
        return send_error("User not found")
    return send_data(user)


