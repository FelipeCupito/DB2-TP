from backendPixie.app.database import banks_accounts_collection as db
from backendPixie.app.models import Bank


def create(bank: Bank):
    bank_data = bank.model_dump()
    result = db.insert_one(bank_data)
    if result.acknowledged:
        bank_data.update({"_id": str(result.inserted_id)})
        bank = Bank(**bank_data)
        return bank
    return None


def check_bank_port(bank):
    return db.find_one({'port': bank.port}) is not None


def check_bank_exist(bank_port: int) -> bool:
    return db.find_one({'port': bank_port}) is not None
