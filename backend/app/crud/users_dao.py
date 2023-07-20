from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from ..models import User


def create(user, db):
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as error:
        raise error
    except SQLAlchemyError as error:
        raise error
    return user


def get_by_cbu(cbu, db):
    return db.query(User).filter(User.cbu == cbu).first()


def get_by_alias(alias_type, db):
    return db.query(User).filter(User.alias_type == alias_type).first()
