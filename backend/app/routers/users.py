from fastapi import APIRouter
from backend.app.crud import users_dao

from backend.app.models import User, Response
from backend.app.routers.utils import _send_data, _send_error

router = APIRouter()


@router.post("/", response_model=Response)
def create_user(user: User):
    if users_dao.check_cbu(user):
        return _send_error("CBU already exists")
    if users_dao.check_alias(user.alias):
        return _send_error("Alias already exists")

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


