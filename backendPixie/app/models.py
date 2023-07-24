from datetime import datetime

from pydantic import BaseModel, model_validator
from enum import Enum
import bcrypt

_ENCODING = 'utf-8'


class AliasType(str, Enum):
    EMAIL = "email"
    PHONE = "phone"
    NICKNAME = "nickname"


def _hash(password: str):
    return bcrypt.hashpw(password.encode(_ENCODING), bcrypt.gensalt()).decode(_ENCODING)


class User(BaseModel):
    _id: str
    alias_type: AliasType
    alias: str
    password: str
    name: str
    cuit: str
    cbu: str
    bank_port: int

    def hash_pass(self):
        self.password = _hash(self.password)

    def pass_matches(self, password: str):
        return bcrypt.checkpw(password.encode(_ENCODING), self.password.encode(_ENCODING))


class Bank(BaseModel):
    _id: str
    name: str
    port: int

    @model_validator(mode='after')
    def port_validation(self) -> 'Bank':
        port = self.port
        if port is None:
            raise ValueError("Port debe ser asignado antes de validar")

        if port < 1023 or port > 65535:
            raise ValueError("Port debe estar entre 0 y 65535")
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Banco Santander",
                "port": "1234",
            }
        }


class Transaction(BaseModel):
    _id: str
    date: datetime = datetime.now()
    from_cbu: str
    to_cbu: str
    amount: float
