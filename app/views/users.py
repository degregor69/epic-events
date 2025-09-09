from getpass import getpass
from app.config import get_db
from app.controllers.users import login_user, create_user, update_user
from app.controllers.roles import get_all_roles
from app.utils.io import ask
from app.utils.permissions import is_management


def login_view(db=None):
    db = db or next(get_db())
    email = input("Email: ")
    password = getpass("Password: ")
    success, message, user = login_user(db, email, password)
    if not success and not user:
        print(f"❌ {message}")
        return login_view(db=db)

    print(f"✅ {message}")
    role = user.role.name
    print(f"\n👤 Connecté en tant que {user.email} ({role})")
    return user


def get_create_user_data(roles) -> dict:
    name = ask("Enter user full name: ")
    email = ask("Enter user email: ")
    employee_number = int(ask("Enter employee number: "))

    print("Available roles:")
    for i, role in enumerate(roles, start=1):
        print(f"{i}. {role.name}")
    role_choice = int(ask("Choose role (number): ")) - 1
    role_id = roles[role_choice].id

    password = ask("Enter password: ")

    return {
        "name": name,
        "email": email,
        "employee_number": employee_number,
        "role_id": role_id,
        "password": password,
    }


@is_management
def create_user_view(user, db=None):
    db = db or next(get_db())
    roles = get_all_roles(db)
    creation_data = get_create_user_data(roles)

    created_user = create_user(
        db=db,
        name=creation_data.get("name"),
        email=creation_data.get("email"),
        password=creation_data.get("password"),
        role_id=creation_data.get("role_id"),
        employee_number=creation_data.get("employee_number"),
    )

    print(
        f"✅ User {created_user.name} ({created_user.email}) created successfully "
        f"with role {creation_data.get('role_id')} created by {user.name}"
    )
    return created_user


def get_update_user_data(roles) -> dict:
    user_id = int(ask("Enter the ID of the user to update: "))

    name = ask("New full name (leave empty to skip): ") or None
    email = ask("New email (leave empty to skip): ") or None
    employee_number_input = ask("New employee number (leave empty to skip): ")
    employee_number = int(employee_number_input) if employee_number_input else None

    print("Available roles:")
    for i, role in enumerate(roles, start=1):
        print(f"{i}. {role.name}")
    role_choice_input = ask("Choose new role (number, leave empty to skip): ")
    role_id = roles[int(role_choice_input) - 1].id if role_choice_input else None

    return {
        "user_id": user_id,
        "name": name,
        "email": email,
        "employee_number": employee_number,
        "role_id": role_id,
    }


@is_management
def update_user_view(current_user, db=None):
    db = db or next(get_db())
    roles = get_all_roles(db)

    update_data = get_update_user_data(roles)
    user_id = update_data.pop("user_id")

    updated_user = update_user(db, user_id, update_data)
    print(f"✅ User {updated_user.name} updated successfully")
    return updated_user
