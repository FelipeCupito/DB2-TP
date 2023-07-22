from typing import Optional, Any

from bson import ObjectId
from pydantic import BaseModel
from enum import Enum


class AliasType(str, Enum):
    CUIT = "cuit"
    CBU = "cbu"
    ID = "_id"


class User(BaseModel):
    _id: str
    alias_type: AliasType
    password: str
    name: str
    cuit: str
    cbu: str
    bank_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "alias_type": "cbu",
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
    port: str


class Transaction(BaseModel):
    _id: str
    date: str
    from_alias_id: str
    to_alias_id: str
    amount: int


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
