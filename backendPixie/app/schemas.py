from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel

from app.models import User


class AliasTransaction(BaseModel):
    date: datetime = datetime.now()
    from_alias: str
    password: str
    to_alias: str
    amount: int

    class Config:
        json_schema_extra = {
            "example": {
                "from_alias": "mauri658",
                "to_alias": "sol2001",
                "amount": 100,
                "password": "myPass",
            }
        }


class CbuTransaction(BaseModel):
    date: datetime = datetime.now()
    from_cbu: str
    password: str
    to_cbu: str
    amount: int

    class Config:
        json_schema_extra = {
            "example": {
                "from_cbu": "1115698756125879562145",
                "to_cbu": "2587965879254687952454",
                "amount": 100,
                "password": "myPass"
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


class TransactionHistory(BaseModel):
    date: datetime
    from_user: UserHistory
    to_user: UserHistory
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
