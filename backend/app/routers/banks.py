from fastapi import APIRouter
from backend.app.crud import banks_dao

from backend.app.models import Bank
from backend.app.routers.utils import send_error, send_data
from backend.app.schemas import Response

router = APIRouter()


@router.post("/bank", response_model=Response)
def create_bank(bank: Bank):
    if banks_dao.check_bank_port(bank):
        return send_error("Bank port already exists")

    bank = banks_dao.create(bank)
    return send_data(bank)
