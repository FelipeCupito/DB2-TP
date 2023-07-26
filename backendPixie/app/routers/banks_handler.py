import requests
import json
from app.schemas import CbuTransaction, AliasTransaction
from app.crud import users_dao
from app.models import User

from app.crud import transactions_dao

HTTP_PROTOCOL = "http://"
HOST = "127.0.0.1"


def get_user_balance(user: User) -> (bool, float):
    url = HTTP_PROTOCOL + HOST + ":" + str(user.bank_port) + "/users" + "/" + user.cbu + "/balance"

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException:
        return False, 0

    if response.status_code != 200:
        return False, 0

    return True, float(response.content)


def _check_balance(user: User, amount: float) -> (bool, str):
    status, balance = get_user_balance(user)
    if not status:
        return False, "Error getting balance"

    if balance - amount >= 0:
        return True, "Success"

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


def _pay_back(cbu_transaction: CbuTransaction) -> (bool, str):
    """
    Pays back the transaction
    le devulve la plata al origen, pixie se hace pasar por un usuario
    """
    # buscos el uruarios origen
    from_user = users_dao.get_by_cbu(cbu_transaction.from_cbu)

    # creo la url para la api del banco del usuario origen
    from_url = HTTP_PROTOCOL + HOST + ":" + str(from_user.bank_port) + "/transactions" + "/charge"

    # creo el payload para la api del banco del usuario origen
    from_payload = {
        "cbu": cbu_transaction.from_cbu,
        "amount": cbu_transaction.amount,
    }

    # Hago la llamada a la api del banco del usuario origen
    try:
        from_response = requests.post(from_url, data=json.dumps(from_payload))
    except requests.exceptions.RequestException:
        return False, "Error in from_bank"

    if from_response.status_code != 200:
        return False, "Error in from_bank"

    return True, "Success"


def pay_by_cbu(cbu_transaction: CbuTransaction) -> (bool, str):
    from_user = users_dao.get_by_cbu(cbu_transaction.from_cbu)
    to_user = users_dao.get_by_cbu(cbu_transaction.to_cbu)

    if not from_user.pass_matches(cbu_transaction.password):
        return False, "Password does not match"

    status, msg = _check_balance(from_user, cbu_transaction.amount)
    if not status:
        return False, msg

    from_url = HTTP_PROTOCOL + HOST + ":" + str(from_user.bank_port) + "/transactions" + "/pay"
    to_url2 = HTTP_PROTOCOL + HOST + ":" + str(to_user.bank_port) + "/transactions" + "/charge"

    from_payload = {
        "cbu": cbu_transaction.from_cbu,
        "amount": cbu_transaction.amount,
    }

    to_payload = {
        "cbu": cbu_transaction.to_cbu,
        "amount": cbu_transaction.amount,
    }

    try:
        from_response = requests.post(from_url, data=json.dumps(from_payload))
    except requests.exceptions.RequestException:
        return False, "Error in from_bank"

    if from_response.status_code != 200:
        return False, "Error in from_bank"

    try:
        to_response = requests.post(to_url2, data=json.dumps(to_payload))
    except requests.exceptions.RequestException:
        _pay_back(cbu_transaction)
        return False, "Error in to_bank"

    if to_response.status_code != 200:
        _pay_back(cbu_transaction)
        return False, "Error in to_bank"

    return True, "Success"
