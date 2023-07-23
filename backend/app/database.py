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
    db = SessionLocal()
    info = []
    info.append(User(name="Malena Vasquez", birthday="16/10/1999", genre="F", cuit="27421942256", cbu="1050025025489632154845", phone="1153145294", email="mavasquez@itba.edu.ar", balance=50000))
    info.append(User(name="Sol Anselmo", birthday="28/01/2001", genre="F", cuit="27432540494", cbu="1112222344444444444443", phone="1158382184", email="soanselmo@itba.edu.ar", balance=60000))
    info.append(User(name="Felipe Cupito", birthday="24/09/1999", genre="M", cuit="27421037476", cbu="2012322344544444244443", phone="1123135744", email="fcupito@itba.edu.ar", balance=30000))
    info.append(User(name="Juan Lopez", birthday="03/04/2000", genre="M", cuit="273403512", cbu="20123222502544442747443", phone="1150153974", email="juanlopezz@gmail.edu.ar", balance=40000))

    for i in info:
        db.add(i)
        db.commit()

    for i in info:
        db.refresh(i)


def create_db():
    Base.metadata.create_all(engine)
    if shouldPopulate:
        print("populated")
        populate_db()
    else:
        print("not populated")



