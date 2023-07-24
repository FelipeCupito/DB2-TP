from typing import Optional
from app.models import User
from app.database import user_collection as db
from app.crud import banks_dao
from app.schemas import NewUser


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


def _get_model_user(new_user: NewUser) -> User:
    bank_port = banks_dao.get_bank_port(new_user.bank_name)
    return User(
        alias_type=new_user.alias_type,
        alias=new_user.alias,
        password=new_user.password,
        name=new_user.name,
        cuit=new_user.cuit,
        cbu=new_user.cbu,
        bank_port=bank_port,
    )


def create(new_user: NewUser) -> Optional[User]:
    user = _get_model_user(new_user)
    user.hash_pass()
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


def check_password(cbu, password):
    user = get_by_cbu(cbu)
    if user is None:
        return False
    return user.pass_matches(password)