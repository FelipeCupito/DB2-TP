import requests
import json
from app.schemas import CbuTransaction, AliasTransaction
from app.crud import users_dao
from app.models import User

HTTP_PROTOCOL = "http://"
HOST = "127.0.0.1"


def _check_balance(user: User, amount: float) -> (bool, str):
    url = HTTP_PROTOCOL + HOST + ":" + str(user.bank_port) + "/users" + "/" + user.cbu + "/balance"
    response = requests.get(url)
    if response.status_code != 200:
        return False, "Error in bank"

    response.json()

    if float(response.content) - amount >= 0 >= 0:
        return True

    return False, "Not enough balance"


def pay_by_alias(alias_transaction: AliasTransaction) -> (bool, str):
    from_cbu = users_dao.get_by_alias(alias_transaction.from_alias).cbu
    to_cbu = users_dao.get_by_alias(alias_transaction.to_alias).cbu
    cbu_transaction = CbuTransaction(
        date=alias_transaction.date,
        from_cbu=from_cbu,
        to_cbu=to_cbu,
        amount=alias_transaction.amount,
        password=alias_transaction.password
    )

    return pay_by_cbu(cbu_transaction)


def pay_by_cbu(cbu_transaction: CbuTransaction) -> (bool, str):
    from_user = users_dao.get_by_cbu(cbu_transaction.from_cbu)
    to_user = users_dao.get_by_cbu(cbu_transaction.to_cbu)

    if not from_user.pass_matches(cbu_transaction.password):
        return False, "Password does not match"

    err, msg = _check_balance(from_user, cbu_transaction.amount)
    if err:
        return False, msg

    url1 = HTTP_PROTOCOL + HOST + ":" + str(from_user.bank_port) + "/transactions" + "/" + from_user.cbu + "/pay"
    url2 = HTTP_PROTOCOL + HOST + ":" + str(to_user.bank_port) + "/transactions" + "/" + to_user.cbu + "/charge"

    payload = {
        "amount": cbu_transaction.amount,
    }

    from_response = requests.post(url1, data=json.dumps(payload))
    if from_response.status_code != 200:
        return False, "Error in from bank"

    to_response = requests.post(url2, data=json.dumps(payload))
    if to_response.status_code != 200:
        return False, "Error in to bank"

    return True, "Success"
