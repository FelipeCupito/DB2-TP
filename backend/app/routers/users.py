from fastapi import APIRouter
from backend.app.crud import users_dao
from typing import Any

from backend.app.models import User, AliasType, Response

router = APIRouter()


@router.post("/", response_model=Response)
def create_user(user: User):
    user = users_dao.create(user)
    return _send_data(user)


@router.get("/cbu/{cbu}", response_model=Response)
def read_user_by_cbu(cbu: str):
    user = users_dao.get_by_cbu(cbu)
    if user is None:
        return _send_error("User not found")
    return _send_data(user)


@router.get("/alias/{alias_type}", response_model=Response)
def read_user_by_alias(alias_type: AliasType, alias: str):
    if not isinstance(alias_type, AliasType):
        return _send_error("alias_type must be an instance of AliasType Enum")
    user = users_dao.get_by_alias(alias_type, alias)
    if user is None:
        return _send_error("User not found")
    return _send_data(user)


def _send_error(msg: str) -> Response:
    return Response(
        status_code=404,
        response_type="error",
        description=msg,
        data=None,
    )


def _send_data(data: Any) -> Response:
    return Response(
        status_code=200,
        response_type="success",
        description="Operation successful",
        data=data
    )
