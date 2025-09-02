import json

from sqlalchemy.orm import Session

from app.models import User
from app.utils.security import hash_password, verify_password, create_access_token


def create_user(db, name, email, password, team, employee_number):
    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        team=team,
        employee_number=employee_number,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def login(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise Exception("Invalid credentials")

    token = create_access_token(user.email)

    with open("token.json", "w") as f:
        json.dump({"token": token}, f)

    return token
