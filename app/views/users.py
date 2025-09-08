from getpass import getpass

from app.config import get_db
from app.controllers.users import login_user, create_user
from app.controllers.roles import get_all_roles
from app.utils.permissions import is_management


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


@is_management
def create_user_view(user):
    db = next(get_db())

    name = input("Enter user full name: ")
    email = input("Enter user email: ")
    employee_number = input("Enter employee number: ")

    roles = get_all_roles(db)
    print("Available roles:")
    for i, role in enumerate(roles, start=1):
        print(f"{i}. {role.name}")
    role_choice = int(input("Choose role (number): ")) - 1
    role_id = roles[role_choice].id

    password = input("Enter password: ")

    created_user = create_user(
        db=db,
        name=name,
        email=email,
        password=password,
        role_id=role_id,
        employee_number=int(employee_number),
    )

    print(
        f"✅ User {created_user.name} ({created_user.email}) created successfully with role {roles[role_choice].name} created by {user.name}"
    )
