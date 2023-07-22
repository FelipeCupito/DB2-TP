from sqlalchemy.exc import SQLAlchemyError

from backend.app.database import User


def pay(cbu, amount, db):
    user = db.query(User).filter(User.cbu == cbu).first()
    user.balance -= amount

    try:
        db.commit()
        db.refresh(user)
    except SQLAlchemyError:
        raise

    return user.balance


def charge(cbu, amount, db):
    user = db.query(User).filter(User.cbu == cbu).first()
    user.balance += amount

    try:
        db.commit()
        db.refresh(user)
    except SQLAlchemyError:
        raise

    return user.balance
