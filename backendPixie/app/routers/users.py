from fastapi import APIRouter
from app.crud import users_dao, banks_dao
from app.routers import banks_handler

from app.routers.utils import send_data, send_error
from app.schemas import Response, NewUser

router = APIRouter()


@router.post("/", response_model=Response)
def create_user(new_user: NewUser):
    if users_dao.check_cbu_exist(new_user.cbu):
        return send_error("CBU already exists")
    if users_dao.check_alias_exist(new_user.alias):
        return send_error("Alias already exists")
    if not banks_dao.check_bank_name_exist(new_user.bank_name):
        return send_error("Bank does not exist")

    user = users_dao.create(new_user)
    return send_data(user)


@router.get("/cbu/{cbu}", response_model=Response)
def read_user_by_cbu(cbu: str, password: str):
    user = users_dao.get_by_cbu(cbu)
    if user is None:
        return send_error("User not found")
    if not user.pass_matches(password):
        return send_error("Password does not match")
    return send_data(user)


@router.get("/alias/{alias_type}", response_model=Response)
def read_user_by_alias(alias: str, password: str):
    user = users_dao.get_by_alias(alias)
    if user is None:
        return send_error("User not found")
    if not user.pass_matches(password):
        return send_error("Password does not match")
    return send_data(user)


@router.get("/{cbu}/balance", response_model=Response)
def get_balance(cbu: str, password: str):
    user = users_dao.get_by_cbu(cbu)
    if user is None:
        return send_error("User not found")
    if not user.pass_matches(password):
        return send_error("Password does not match")

    status, balance = banks_handler.get_user_balance(user)
    if not status:
        return send_error("Error in bank")

    return send_data(balance)
