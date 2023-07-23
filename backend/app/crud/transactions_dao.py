from sqlalchemy.exc import SQLAlchemyError

from backend.app.database import User


def pay(cbu, amount, db):
    user = db.query(User).filter(User.cbu == cbu).first()
    if user:
        balance = user.balance
    else:
        return -1  # No existe el usuario
    if balance >= amount:
        balance -= amount
    else:
        return -2  # No hay saldo

    try:
        db.commit()
        db.refresh(user)
    except SQLAlchemyError:
        raise

    return balance


def charge(cbu, amount, db):
    user = db.query(User).filter(User.cbu == cbu).first()
    if user:
        balance = user.balance
    else:
        return -1  # No existe el usuario

    balance += amount

    try:
        db.commit()
        db.refresh(user)
    except SQLAlchemyError:
        raise

    return balance
