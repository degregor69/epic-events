from getpass import getpass

from app.config import get_db
from app.controllers.users import login_user


def login_view():
    email = input("Email: ")
    password = getpass("Password: ")
    db = next(get_db())
    success, message = login_user(db, email, password)
    print("✅" if success else "❌", message)
