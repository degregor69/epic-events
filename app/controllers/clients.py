from sqlalchemy.orm import Session

from app.models import Client


def list_all_clients(db: Session):
    return db.query(Client).all()
