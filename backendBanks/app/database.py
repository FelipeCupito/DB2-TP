import json
import sys

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Float
from app.config import settings


port = sys.argv[2] if len(sys.argv) > 2 else 5432

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{int(port)}/{settings.POSTGRES_DB}"

print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
inspector = inspect(engine)

shouldPopulate = not inspector.has_table('Users')


class User(Base):
    __tablename__ = "Users"
    name = Column(String, nullable=False)
    birthday = Column(String)
    genre = Column(String)
    cuit = Column(String, unique=True, nullable=False)
    cbu = Column(String, primary_key=True, unique=True, nullable=False)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    balance = Column(Float, nullable=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def populate_db():
    file_path = sys.argv[3] if len(sys.argv) > 3 else None
    if file_path is None:
        raise Exception("File path not supported")

    with open(file_path, 'r') as file:
        data = json.load(file)

    db = SessionLocal()

    for user_data in data['users']:
        user = User(**user_data)
        db.add(user)

    db.commit()
    db.close()


def create_db():
    Base.metadata.create_all(engine)
    if shouldPopulate:
        populate_db()
        print("DB populated")
    else:
        print("DB already populated")



