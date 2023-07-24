from pymongo import MongoClient
from app.config import settings
from app.models import Bank, User, hash

COLLECTIONS_USER = "users"
COLLECTIONS_TRANSACTION = "transactions"
COLLECTIONS_BANK = "banks_accounts"

DATABASE_URL = f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_DB_HOSTNAME}:{settings.DATABASE_PORT}"

print(DATABASE_URL)

client = MongoClient(DATABASE_URL)
db = client[settings.MONGO_DB_DBNAME]


def _create_banks_accounts():
    db.create_collection(COLLECTIONS_BANK)
    bank1_data = {
        "name": "Banco Santander",
        "port": "8080",
    }
    bank2_data = {
        "name": "Banco Patagonia",
        "port": "8090",
    }
    bank1 = Bank(**bank1_data)
    bank2 = Bank(**bank2_data)
    db[COLLECTIONS_BANK].insert_one(bank1.model_dump())
    db[COLLECTIONS_BANK].insert_one(bank2.model_dump())


def _create_transactions():
    db.create_collection(COLLECTIONS_TRANSACTION)


def _create_user():
    db.create_collection(COLLECTIONS_USER)
    user1_data = {
        "alias_type": "email",
        "alias": "fcupito@itba.edu.ar",
        "password": hash("myPass"),
        "name": "Felipe Cupito",
        "cuit": "27421037476",
        "cbu": "2012322344544444244443",
        "bank_port": "8080",
    }
    user2_data = {
        "alias_type": "phone",
        "alias": "1153145294",
        "password": hash("pass"),
        "name": "Malena Vasquez",
        "cuit": "27421942256",
        "cbu": "1050025025489632154845",
        "bank_port": "8080",
    }
    user3_data = {
        "alias_type": "phone",
        "alias": "1168325648",
        "password": hash("pass1234"),
        "name": "Lucia Martinez",
        "cuit": "27441737251",
        "cbu": "1050055025489573154848",
        "bank_port": "8090",
    }
    user4_data = {
        "alias_type": "nickname",
        "alias": "maxperez89",
        "password": hash("password"),
        "name": "Maximiliano Perez",
        "cuit": "27500676437",
        "cbu": "1112222398765432154898",
        "bank_port": "8090",
    }
    user1 = User(**user1_data)
    user2 = User(**user2_data)
    user3 = User(**user3_data)
    user4 = User(**user4_data)
    db[COLLECTIONS_USER].insert_one(user1.model_dump())
    db[COLLECTIONS_USER].insert_one(user2.model_dump())
    db[COLLECTIONS_USER].insert_one(user3.model_dump())
    db[COLLECTIONS_USER].insert_one(user4.model_dump())


def _create_collections_if_not_exists():
    """Create all collections if they don't exist."""
    if COLLECTIONS_BANK not in db.list_collection_names():
        _create_banks_accounts()
    if COLLECTIONS_TRANSACTION not in db.list_collection_names():
        _create_transactions()
    if COLLECTIONS_USER not in db.list_collection_names():
        _create_user()


# Initialize DB
_create_collections_if_not_exists()

user_collection = db[COLLECTIONS_USER]
transactions_collection = db[COLLECTIONS_TRANSACTION]
banks_accounts_collection = db[COLLECTIONS_BANK]
