from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Float, Date
from backend.app.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

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
    birthday = Column(Date)
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
    db = SessionLocal()
    info = []

    info.append(User(cbu="0004239328123719132482", accountType=1, name="Agustin Mattiussi",
                                email="amattiussi@itba.edu.ar", password=hash_password("pass123"), cuit="20-43084142-5",
                                phoneNumber="+54 911 3896-0800", balance=50000.00))

    for i in info:
        db.add(i)
        db.commit()

    for i in info:
        db.refresh(i)


def create_db():
    Base.metadata.create_all(engine)

    if (shouldPopulate):
        populate_db()


create_db()