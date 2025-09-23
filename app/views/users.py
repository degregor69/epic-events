from getpass import getpass
from app.config import get_db
from app.services.users import UserService
from app.services.roles import RoleService
from app.models import User
from app.utils.io import ask
from app.utils.permissions import is_management


def login_view(db=None):
    db = db or next(get_db())
    email = input("Email: ")
    password = getpass("Password: ")
    users_service = UserService(db=db)
    success, message, user = users_service.login_user(email, password)
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


def create_user_view(current_user, db=None):

    db = db or next(get_db())
    roles_service = RoleService(db=db)
    roles = roles_service.get_all_roles()
    data = get_create_user_data(roles)
    users_service = UserService(db=db)
    return users_service.create_user(
        current_user,
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role_id=data["role_id"],
        employee_number=data["employee_number"],
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


def update_user_view(current_user, db=None):
    db = db or next(get_db())
    roles_service = RoleService(db)
    roles = roles_service.get_all_roles()

    update_data = get_update_user_data(roles)
    user_id = update_data.pop("user_id")

    users_service = UserService(db=db)
    updated_user = users_service.update_user(current_user, user_id, update_data)
    print(f"✅ User {updated_user.name} updated successfully")
    return updated_user


def get_user_id_to_be_deleted(users: list[User]):
    print("\nWhich user do you want to delete ?")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.id} {user.email}")

    row_number = input("Entrer the row number :")
    return int(row_number)


def delete_user_view(current_user, db=None):
    db = db or next(get_db())
    users = db.query(User).all()
    row_number = get_user_id_to_be_deleted(users)
    user_to_delete = users[int(row_number) - 1]
    users_service = UserService(db=db)
    users_service.delete_user(current_user, user_id=user_to_delete.id)
    print(f"User : {user_to_delete.id} | {user_to_delete.name} deleted")
