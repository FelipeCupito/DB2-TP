# import requests
# import json
# from app.schemas import CbuTransaction
# from app.crud import users_dao
# from app.models import User
#
# HTTP_PROTOCOL = "http://"
# HOST = "127.0.0.1"

# def _check_balance(user: User, amount: float) -> bool:
#     url = HTTP_PROTOCOL + HOST + ":" + str(user.bank_port) + "/users" + "/" + user.cbu + "/balance"
#     response = requests.get(url)
#     if response.status_code != 200:
#         return False
#     print(response.json())
#
#     #if response - amount >= 0:
#     #    return True
#     return True
#
# def pay_by_cbu(cbu_transaction: CbuTransaction) -> bool:
#     user1 = users_dao.get_by_cbu(cbu_transaction.from_cbu)
#     user2 = users_dao.get_by_cbu(cbu_transaction.to_cbu)
#
#     if not _check_balance(user1, cbu_transaction.amount):
#         return False #No hay saldo
#
#     url1 = HTTP_PROTOCOL + HOST + ":" + str(user1.bank_port) + "/transactions" + "/" + user1.cbu + "/pay"
#     url2 = HTTP_PROTOCOL + HOST + ":" + str(user2.bank_port) + "/transactions" + "/" + user2.cbu + "/charge"
#
#     payload = {
#         "amount": 1250  # Actualiza esto con la cantidad exacta que quieras enviar
#     }
#
#     response1 = requests.post(url1, data=json.dumps(payload))
#     response2 = requests.post(url2, data=json.dumps(payload))
#
#     print(response1.status_code)
#     print(response1.json())
#     print(response2.status_code)
#     print(response2.json())