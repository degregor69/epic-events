from sqlalchemy.orm import Session
from app.models import Contract


def get_all_contracts(db: Session):
    return db.query(Contract).all()
