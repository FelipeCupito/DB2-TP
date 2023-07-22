from fastapi import APIRouter
from backend.app.crud import transactions_dao
from backend.app.models import Transaction

router = APIRouter()


@router.post("/pay-cbu", response_model=Transaction)
def pay_by_cbu(from_cbu: str, to_cbu: str, amount: float):
    return transactions_dao.pay_by_cbu(from_cbu, to_cbu, amount)


@router.post("/pay-alias", response_model=Transaction)
def pay_by_cbu(from_alias: str, to_alias: str, amount: float):
    return transactions_dao.pay_by_alias(from_alias, to_alias, amount)
