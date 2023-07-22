from sqlalchemy import Column, String, Float, Date
from sqlalchemy import ForeignKey

from database import Base, engine


class User(Base):
    __tablename__ = "users"
    name = Column(String, nullable=False)
    birthday = Column(Date)
    genre = Column(String)
    cuit = Column(String, unique=True, nullable=False)
    cbu = Column(String, primary_key=True, unique=True, nullable=False)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    balance = Column(Float, nullable=False)

    __table_args__ = {'extend_existing': True}


Base.metadata.create_all(bind=engine)
