from typing import Optional

from backend.app.database import transactions_collection as db
from backend.app.models import Transaction
from backend.app.schemas import CbuTransaction, AliasTransaction, TransactionHistory

from backend.app.crud import users_dao


def pay_by_cbu(cbu_transaction: CbuTransaction) -> Optional[Transaction]:
    transaction = _get_transaction_from_cbu(cbu_transaction).model_dump()
    result = db.insert_one(transaction)
    if result.acknowledged:
        transaction.update({"_id": str(result.inserted_id)})
        transaction = Transaction(**transaction)
        return transaction
    return None


def pay_by_alias(alis_transaction: AliasTransaction) -> Optional[Transaction]:
    transaction = _get_transaction_from_alias(alis_transaction).model_dump()
    result = db.insert_one(transaction)
    if result.acknowledged:
        transaction.update({"_id": str(result.inserted_id)})
        transaction = Transaction(**transaction)
        return transaction
    return None


def get_user_history(cbu: str) -> list[TransactionHistory]:
    to_return = []
    for transaction in db.find({'from_cbu': cbu}):
        from_user = users_dao.get_by_cbu(transaction.from_cbu)
        to_user = users_dao.get_by_cbu(transaction.to_cbu)
        to_return.append(
            TransactionHistory(
                from_user=from_user,
                to_user=to_user,
                amount=transaction.amount,
                date=transaction.date,
            )
        )
    return to_return


def _get_transaction_from_alias(transaction: AliasTransaction) -> Transaction:
    from_cbu = users_dao.get_by_alias(transaction.from_alias).cbu
    to_cbu = users_dao.get_by_alias(transaction.to_alias).cbu
    return Transaction(
        from_cbu=from_cbu,
        to_cbu=to_cbu,
        amount=transaction.amount,
        date=transaction.date,
    )


def _get_transaction_from_cbu(transaction: CbuTransaction) -> Transaction:
    return Transaction(
        from_alias=transaction.from_cbu,
        to_alias=transaction.to_cbu,
        amount=transaction.amount,
        date=transaction.date,
    )
