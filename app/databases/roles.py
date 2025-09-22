from sqlalchemy.orm import Session
from app.models import Role


class RoleDB:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Role).all()
