from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, model_validator
import re

from app.models import User, AliasType

PATTERN_CBU = r'^\d{22}$'
PATTERN_PHONE = r'^\d{10}$'
PATTERN_CUIT = r'^(20|23|24|25|26|27|30|33|34)[0-9]{8}[0-9]{1}$'
PATTERN_EMAIL = r'^[\w.-]+@[\w.-]+.\w+$'


class UserBase(BaseModel):
    id: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "cbu or alias",
                "password": "myPass",
            }
        }


class NewUser(BaseModel):
    alias_type: AliasType
    alias: str
    password: str
    name: str
    cuit: str
    cbu: str
    bank_name: str

    @model_validator(mode='after')
    def validate_alias(self) -> 'NewUser':
        alias_type = self.alias_type
        alias = self.alias

        if not re.match(PATTERN_CBU, self.cbu):
            raise ValueError('CBU must be 22 numbers long')

        if not re.match(PATTERN_CUIT, self.cuit):
            raise ValueError('Must be an existing CUIT')

        if alias_type is None:
            raise ValueError("alias_type debe ser asignado antes del alias")

        if alias_type == AliasType.EMAIL:
            if not re.match(PATTERN_EMAIL, alias):
                raise ValueError("Email inválido")

        elif alias_type == AliasType.PHONE:
            if not re.match(PATTERN_PHONE, alias):
                raise ValueError("Número de teléfono debe contener solo dígitos")

        elif alias_type == AliasType.NICKNAME:
            if not alias.isalnum():
                raise ValueError("El alias sóolo puede contener caracteres alfanuméricos")

        return self

    class Config:
        json_schema_extra = {
            "example": {
                "alias_type": "email",
                "alias": "pepe@email.com",
                "password": "myPass",
                "name": "Pepe",
                "cuit": "20432540493",
                "cbu": "1115698756125879562145",
                "bank_name": "Banco Santander",
            }
        }


class AliasTransaction(BaseModel):
    date: datetime = datetime.now()
    from_alias: str
    password: str
    to_alias: str
    amount: float
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "from_alias": "mauri658",
                "to_alias": "sol2001",
                "amount": 100,
                "password": "myPass",
                "description": "payment description"
            }
        }


class CbuTransaction(BaseModel):
    date: datetime = datetime.now()
    from_cbu: str
    password: str
    to_cbu: str
    amount: float
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "from_cbu": "1115698756125879562145",
                "to_cbu": "2587965879254687952454",
                "amount": 100,
                "password": "myPass",
                "description": "payment description"
            }
        }


class UserHistory(BaseModel):
    alias: str
    name: str
    cbu: str

    @classmethod
    def from_user(cls, user: User) -> 'UserHistory':
        return cls(
            alias=user.alias,
            name=user.name,
            cbu=user.cbu,
        )

    class Config:
        json_schema_extra = {
            "example": {
                "alias": "mauri658",
                "name": "Mauro Garcia",
                "cbu": "1115698756125879562145",
            }
        }


class TransactionHistory(BaseModel):
    date: datetime
    from_user: UserHistory
    to_user: UserHistory
    amount: int
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2021-06-01T12:00:00",
                "from_user": {
                    "alias": "mauri658",
                    "name": "Mauro Garcia",
                    "cbu": "1115698756125879562145",
                },
                "to_user": {
                    "alias": "sol2001",
                    "name": "Sol Garcia",
                    "cbu": "2587965879254687952454",
                },
                "amount": 100,
                "description": "payment description"
            }
        }


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data",
            }
        }
