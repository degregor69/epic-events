from sqlalchemy.orm import Session
from app.models import User
from app.databases.users import UserDB
from app.utils.permissions import is_management
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    save_tokens,
)


class UserService:
    def __init__(self, db: Session):
        self.user_db = UserDB(db)

    @is_management
    def create_user(
        self, current_user, name, email, password, role_id, employee_number
    ):
        user = User(
            name=name,
            email=email,
            hashed_password=hash_password(password),
            role_id=role_id,
            employee_number=employee_number,
        )
        return self.user_db.add(user)

    @is_management
    def update_user(self, current_user, user_id: int, updates: dict):
        user = self.user_db.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        return self.user_db.update(user, updates)

    @is_management
    def delete_user(self, current_user, user_id: int):
        user = self.user_db.get_by_id(user_id)
        print(f"Utilisateur supprimé: {user}")
        if not user:
            raise Exception("User to be deleted not found")
        self.user_db.delete(user)

    def login_user(self, email: str, password: str):
        user = self.user_db.get_by_email(email)
        if not user:
            return False, "User not found", None
        if not verify_password(password, user.hashed_password):
            return False, "Wrong password", None

        access_token = create_access_token(user.email)
        refresh_token = create_refresh_token(user.email)

        save_tokens({"access_token": access_token, "refresh_token": refresh_token})
        return True, "Login successful", user

    def get_all_users(self):
        return self.user_db.get_all()
