from sqlalchemy.orm import Session

from app.models import Client


def get_all_clients(db: Session):
    return db.query(Client).all()
