from fastapi import APIRouter
from backend.app.crud import banks_dao

from backend.app.models import Bank, Response
from backend.app.routers.utils import _send_error, _send_data

router = APIRouter()


@router.post("/bank", response_model=Response)
def create_bank(bank: Bank):
    if banks_dao.check_bank_port(bank):
        return _send_error("Bank port already exists")

    bank = banks_dao.create(bank)
    return _send_data(bank)
