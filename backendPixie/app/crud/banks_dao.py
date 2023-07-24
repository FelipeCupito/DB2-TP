from typing import Optional

from app.database import banks_accounts_collection as db
from app.models import Bank


def create(bank: Bank):
    bank_data = bank.model_dump()
    result = db.insert_one(bank_data)
    if result.acknowledged:
        bank_data.update({"_id": str(result.inserted_id)})
        bank = Bank(**bank_data)
        return bank
    return None


def get_bank_port(bank_name: str) -> Optional[int]:
    bank = db.find_one({'name': bank_name})
    if bank is None:
        return None
    return bank['port']


def check_bank_port(bank: Bank):
    return db.find_one({'port': bank.port}) is not None


def check_bank_name(bank: Bank):
    return db.find_one({'name': bank.name}) is not None


def check_bank_name_exist(bank_name: str):
    return db.find_one({'name': bank_name}) is not None
