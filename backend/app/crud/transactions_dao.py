from decimal import Decimal

from sqlalchemy.orm import Session

from backend.app.models import User


def modify_balance_by_cbu(cbu, amount, db: Session):
    user = db.query(User).filter(User.cbu == cbu).first()
    user.balance += Decimal(amount)


def pay_by_cbu(from_cbu, to_cbu, amount, db):
    modify_balance_by_cbu(from_cbu, -amount, db)
    modify_balance_by_cbu(to_cbu, amount, db)
    return None


def pay_by_alias(from_alias, to_alias, amount, db):
    return None
