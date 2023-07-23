import re
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Any


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


class UserBase(BaseModel):
    name: str
    birthday: str
    genre: str
    cuit: str
    cbu: str
    phone: str
    email: EmailStr
    balance: float

    @field_validator('cbu')
    def validate_cbu(cls, v):
        pattern = r'^\d{22}$'
        if not re.match(pattern, v):
            raise ValueError('CBU must be 22 numbers long')
        return v

    @field_validator('phone')
    def validate_phone(cls, v):
        pattern = r'^\d{10}$'
        if not re.match(pattern, v):
            raise ValueError('phone must be 10 numbers long')
        return v

    @field_validator('cuit')
    def validate_cuit(cls, v):
        pattern = r'^(20|23|24|25|26|27|30|33|34)[0-9]{8}[0-9]{1}$'
        if not re.match(pattern, v):
            raise ValueError('Must be an existing CUIT')
        return v

    @field_validator('birthday')
    def validate_birthday(cls, v):
        pattern = r'^([0-2][0-9]|3[0-1])\/(0[1-9]|1[0-2])\/(19[0-9]{2}|2[0-9]{3})$'
        if not re.match(pattern, v):
            raise ValueError('Birthdate must be in format dd/mm/yyyy')
        return v

    @field_validator('genre')
    def validate_genre(cls, v):
        pattern = r'^(F|M|X)$'
        if not re.match(pattern, v):
            raise ValueError('Genre must be F (female), M (male) or X (other)')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Mauro Garcia",
                "birthday": "25/06/1989",
                "genre": "M",
                "cuit": "2021584564",
                "cbu": "2569874523698521458965",
                "phone": "1156950216",
                "email": "maurogarcia@gmail.com",
                "balance": 75000,
            }
        }
