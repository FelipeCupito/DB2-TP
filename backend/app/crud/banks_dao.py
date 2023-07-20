from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from backend.app.models import Bank


def create(name, port, db):
    bank = Bank(name, port)
    try:
        db.add(bank)
        db.commit()
        db.refresh(bank)
    except IntegrityError as error:
        raise error
    except SQLAlchemyError as error:
        raise error
    return bank
