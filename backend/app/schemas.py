import datetime
from typing import Optional, Any
from pydantic import BaseModel
from backend.app.models import User


class AliasTransaction(BaseModel):
    date: datetime = datetime.datetime.now()
    from_alias: str
    to_alias: str
    amount: int

    class Config:
        json_schema_extra = {
            "example": {
                "from_alias_id": "1",
                "to_alias_id": "2",
                "amount": "100",
            }
        }


class CbuTransaction(BaseModel):
    date: datetime = datetime.datetime.now()
    from_cbu: str
    to_cbu: str
    amount: int

    class Config:
        json_schema_extra = {
            "example": {
                "from_cbu_id": "1",
                "to_cbu_id": "2",
                "amount": "100",
            }
        }


class TransactionHistory(BaseModel):
    date: datetime
    from_user: User
    to_user: User
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
