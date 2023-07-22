from typing import Optional
from backend.app.models import User, AliasType
from backend.app.database import user_collection as db


def get_by_cbu(cbu: str) -> Optional[User]:
    user = db.find_one({'cbu': cbu})
    if user is None:
        return None
    return User(**user)


def get_by_alias(alias_type: AliasType, alias: str) -> Optional[User]:
    user = db.find_one({alias_type.value: alias})
    if user is None:
        return None
    return User(**user)


def create(user: User) -> Optional[User]:
    # TODO: Check if user already exists
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
