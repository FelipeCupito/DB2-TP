from fastapi import APIRouter
from backendPixie.app.crud import banks_dao

from backendPixie.app.models import Bank
from backendPixie.app.routers.utils import send_error, send_data
from backendPixie.app.schemas import Response

router = APIRouter()


@router.post("/", response_model=Response)
def create_bank(bank: Bank):
    if banks_dao.check_bank_port(bank):
        return send_error("Bank port already exists")

    bank = banks_dao.create(bank)
    return send_data(bank)
