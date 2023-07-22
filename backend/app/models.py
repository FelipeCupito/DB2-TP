import datetime
from typing import Optional, Any

from pydantic import BaseModel, model_validator
from enum import Enum


class AliasType(str, Enum):
    EMAIL = "email"
    PHONE = "phone"
    NICKNAME = "nickname"


class User(BaseModel):
    _id: str
    alias_type: AliasType
    alias: str
    password: str
    name: str
    cuit: str
    cbu: str
    bank_id: str

    @model_validator(mode='after')
    def validate_alias(self) -> 'User':
        alias_type = self.alias_type
        alias = self.alias

        if alias_type is None:
            raise ValueError("alias_type debe ser asignado antes del alias")

        if alias_type == AliasType.EMAIL:
            if "@" not in alias:
                raise ValueError("Email inválido")

        elif alias_type == AliasType.PHONE:
            if not alias.isdigit():
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
                "cuit": "dldldd",
                "cbu": "1234123",
                "bank_id": "1",
            }
        }


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
                "port": "http://localhost:8000",
            }
        }


class Transaction(BaseModel):
    _id: str
    date: datetime = datetime.datetime.now()
    from_id: str
    to_id: str
    amount: int

