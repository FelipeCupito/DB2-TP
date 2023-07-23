from ..database import User


def get_info(cbu, db):
    return db.query(User).filter(User.cbu == cbu).first()


def get_balance(cbu, db):
    user = db.query(User).filter(User.cbu == cbu).first()
    if user:
        return user.balance
    else:
        return None
