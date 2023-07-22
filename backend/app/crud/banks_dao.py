from backend.app.database import banks_accounts_collection as db
from backend.app.models import Bank


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


def check_bank_exist(bank_id: str) -> bool:
    return db.find_one({'_id': bank_id}) is not None
