from pymongo import MongoClient
from backendPixie.app.config import settings

COLLECTIONS_NAME = ["users", "transactions", "banks_accounts"]
DATABASE_URL = f"mongodb://{settings.MONGO_USERNAME}:{settings.MONGO_PASSWORD}@{settings.MONGO_DB_HOSTNAME}:{settings.DATABASE_PORT}"

client = MongoClient(DATABASE_URL)
db = client[settings.MONGO_DB_DBNAME]


def _populate_db():
    # TODO: implement
    pass


def _create_collections_if_not_exists():
    """Create all collections if they don't exist."""
    for collection in COLLECTIONS_NAME:
        if collection not in db.list_collection_names():
            db.create_collection(collection)


# Initialize DB
_create_collections_if_not_exists()
_populate_db()

user_collection = db["users"]
transactions_collection = db["transactions"]
banks_accounts_collection = db["banks_accounts"]
