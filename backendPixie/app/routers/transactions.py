from fastapi import APIRouter
from app.crud import transactions_dao, users_dao
from app.routers import banks_handler

from app.routers.utils import send_data, send_error
from app.schemas import Response, CbuTransaction, AliasTransaction

router = APIRouter()


@router.post("/pay-cbu", response_model=Response)
def pay_by_cbu(cbu_transaction: CbuTransaction):
    if not users_dao.check_cbu_exist(cbu_transaction.from_cbu):
        return send_error("from CBU does not exist")
    if not users_dao.check_cbu_exist(cbu_transaction.to_cbu):
        return send_error("to CBU does not exist")
    if cbu_transaction.from_cbu == cbu_transaction.to_cbu:
        return send_error("from CBU and to CBU cannot be the same") 
    
    status, msg = banks_handler.pay_by_cbu(cbu_transaction)
    if not status:
        return send_error(msg)

    transaction = transactions_dao.pay_by_cbu(cbu_transaction)

    return send_data(transaction)


@router.post("/pay-alias", response_model=Response)
def pay_by_alias(alias_transaction: AliasTransaction):
    if not users_dao.check_alias_exist(alias_transaction.from_alias):
        return send_error("from Alias does not exist")
    if not users_dao.check_alias_exist(alias_transaction.to_alias):
        return send_error("to Alias does not exist")

    status, msg = banks_handler.pay_by_alias(alias_transaction)
    if not status:
        return send_error(msg)

    transaction = transactions_dao.pay_by_alias(alias_transaction)
    return send_data(transaction)


@router.get("/{cbu}/history", response_model=Response)
def get_user_history(cbu: str):
    if not users_dao.check_cbu_exist(cbu):
        return send_error("CBU does not exist")
    history = transactions_dao.get_user_history(cbu)
    return send_data(history)
