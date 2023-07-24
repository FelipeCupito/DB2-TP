from sqlalchemy.exc import SQLAlchemyError

from app.database import User


def pay(cbu, amount, db):
    user = db.query(User).filter(User.cbu == cbu).first()
    if user:
        balance = user.balance
    else:
        return -1  # No existe el usuario
    if balance >= amount:
        user.balance -= amount
    else:
        return -2  # No hay saldo

    try:
        db.commit()
        db.refresh(user)
    except SQLAlchemyError:
        raise

    return user.balance


def charge(cbu, amount, db):
    user = db.query(User).filter(User.cbu == cbu).first()
    if user:
        user.balance += amount
    else:
        return -1  # No existe el usuario

    try:
        db.commit()
        db.refresh(user)
    except SQLAlchemyError:
        raise

    return user.balance
