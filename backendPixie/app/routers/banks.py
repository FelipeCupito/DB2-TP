from fastapi import APIRouter
from app.crud import banks_dao

from app.models import Bank
from app.routers.utils import send_error, send_data
from app.schemas import Response

router = APIRouter()


@router.post("/", response_model=Response)
def create_bank(bank: Bank):
    if banks_dao.check_bank_port(bank):
        return send_error("Bank port already exists")

    if banks_dao.check_bank_name(bank):
        return send_error("Bank name already exists")

    bank = banks_dao.create(bank)
    return send_data(bank)
