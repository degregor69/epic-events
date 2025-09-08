from getpass import getpass

from app.config import get_db
from app.controllers.users import login_user


def login_view():
    email = input("Email: ")
    password = getpass("Password: ")
    db = next(get_db())
    success, message, user = login_user(db, email, password)
    if not success and not user:
        print(f"❌ {message}")
        login_view()

    print(f"✅ {message}")
    role = user.role.name
    print(f"\n👤 Connecté en tant que {user.email} ({role})")
    return user
