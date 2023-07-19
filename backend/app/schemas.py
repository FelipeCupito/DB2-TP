from pydantic import BaseModel


class UserBase(BaseModel):
    alias_type: str  # hacer que solo pueda de lo tipos validos
    password: str
    name: str
    cuit: str
    cbu: str
    bank_id: str


class Bank(BaseModel):
    id: int
    name: str
    port: str


class Transaction(BaseModel):
    id: int
    date: str
    from_alias_id: int
    to_alias_id: int
    amount: float
