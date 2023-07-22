from fastapi import APIRouter
from backend.app.crud import transactions_dao
from backend.app.schemas import Response, CbuTransaction, AliasTransaction

router = APIRouter()


@router.post("/pay-cbu", response_model=Response)
def pay_by_cbu(transaction: CbuTransaction):
    return transactions_dao.pay_by_cbu(transaction)


@router.post("/pay-alias", response_model=Response)
def pay_by_cbu(transaction: AliasTransaction):
    return transactions_dao.pay_by_alias(transaction)


@router.get("/history/{cbu}", response_model=Response)
def get_user_history(cbu: str):
    return transactions_dao.get_user_history(cbu)
