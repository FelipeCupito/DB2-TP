from sqlalchemy.exc import SQLAlchemyError, IntegrityError


def create(bank, db):
    try:
        db.add(bank)
        db.commit()
        db.refresh(bank)
    except IntegrityError as error:
        raise error
    except SQLAlchemyError as error:
        raise error
    return bank
