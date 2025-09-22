from sqlalchemy.orm import Session
from app.models import User


class UserDB:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        return self.db.get(User, user_id)

    def get_by_email(self, email: str):
        return self.db.query(User).filter_by(email=email).first()

    def add(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, data: dict):
        for attr, value in data.items():
            if hasattr(user, attr) and value is not None:
                setattr(user, attr, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User):
        self.db.delete(user)
        self.db.commit()
