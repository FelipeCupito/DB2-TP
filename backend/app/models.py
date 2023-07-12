from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    _id = Column(String, primary_key=True, unique=True)
    alias_type = Column(String)
    password = Column(PasswordType(schemes=['pbkdf2_sha256']))
    name = Column(String)
    cuit = Column(String)
    cbu = Column(String)
    bank_id = Column(ForeignKey("banks._id"))


class Bank(Base):
    __tablename__ = "banks"
    _id = Column(UUID(as_uuid=True), primary_key=True, unique=True)
    name = Column(String)
    port = Column(String)


class Transaction(Base):
    __tablename__ = "transactions"
    _id = Column(UUID(as_uuid=True), primary_key=True)
    date = Column(DateTime, default=datetime.utcnow)
    from_alias_id = Column(ForeignKey("users._id"))
    to_alias_id = Column(ForeignKey("users._id"))
    amount = Column(Float)
