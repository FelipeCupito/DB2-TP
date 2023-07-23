from typing import Optional
from backendPixie.app.models import User
from backendPixie.app.database import user_collection as db


def get_by_cbu(cbu: str) -> Optional[User]:
    user = db.find_one({'cbu': cbu})
    if user is None:
        return None
    return User(**user)


def get_by_alias(alias: str) -> Optional[User]:
    user = db.find_one({'alias': alias})
    if user is None:
        return None
    return User(**user)


def create(user: User) -> Optional[User]:
    user_data = user.model_dump()
    result = db.insert_one(user_data)
    if result.acknowledged:
        user_data.update({"_id": str(result.inserted_id)})
        user = User(**user_data)
        return user
    return None


def delete(cbu: str) -> bool:
    result = db.Users.delete_one({'cbu': cbu})
    return result.deleted_count > 0


def check_cbu_exist(cbu: str) -> bool:
    return get_by_cbu(cbu) is not None


def check_alias_exist(alias: str) -> bool:
    return get_by_alias(alias) is not None


def check_balance(from_cbu: str, amount: int) -> bool:
    # TODO: implement
    return True
