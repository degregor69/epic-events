from app.config import SessionLocal
from app.models import User
from app.utils.security import hash_password


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
