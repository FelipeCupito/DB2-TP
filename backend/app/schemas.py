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


