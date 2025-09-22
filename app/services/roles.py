from sqlalchemy.orm import Session
from app.databases.roles import RoleDB
from app.models import Role


class RoleService:
    def __init__(self, db: Session):
        self.role_db = RoleDB(db)

    def get_all_roles(self):
        return self.role_db.get_all()
