import json

from sqlalchemy.orm import Session

from app.models import User
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    save_tokens,
)


def create_user(db, name, email, password, role_id, employee_number):
    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role_id=role_id,
        employee_number=employee_number,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        return False, "User not found", None
    if not verify_password(password, user.hashed_password):
        return False, "Wrong password", None

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    save_tokens({"access_token": access_token, "refresh_token": refresh_token})
    return True, "Login successful", user
