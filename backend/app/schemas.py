from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    birthday: str
    genre: str
    cuit: str
    cbu: str
    phone: str
    email: str
    balance: float


class Transaction(BaseModel):
    date: str
    from_alias: str
    to_alias: str
    amount: float

