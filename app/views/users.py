from getpass import getpass
from app.config import get_db
from app.services.users import UserService
from app.services.roles import RoleService
from app.models import User
from app.utils.io import ask


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
    name = input(
"Entrez le nom complet de l'utilisateur : ")
    email = input(
"Entrez l'email : ")
    employee_number = int(input(
"Entrez le numéro d'employé : "))

    print("Rôles disponibles :")
    for i, role in enumerate(roles, start=1):
        print(f"{i}. {role.name}")
    role_choice = int(input(
"Choisissez le rôle en entrant le numéro : ")) - 1
    role_id = roles[role_choice].id

    password = input(
"Entrez le mot de passe : ")

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
    users_service = UserService(db=db)
    data = get_create_user_data(roles)
    role_id = data.get("role_id")
    created_user = users_service.create_user(
        current_user,
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role_id=data["role_id"],
        employee_number=data["employee_number"],
    )
   
    selected_role = next(role for role in roles if role.id == role_id)


    print(
        f"Utilisateur {created_user.name} ({created_user.email}) créé avec succès "
        f"avec le role : {selected_role.name} créé par {current_user.name}"
    )
    return created_user


def get_update_user_data(roles) -> dict:

    name = input(
"Nouveau nom (laissez blanc pour passer): ") or None
    email = input(
"Nouvel email (laissez blanc pour passer) : ") or None
    employee_number_input = input(
"Nouveau numéro d'employé (laissez blanc pour passer) : ")
    employee_number = int(employee_number_input) if employee_number_input else None

    print("Rôles disponibles :")
    for i, role in enumerate(roles, start=1):
        print(f"{i}. {role.name}")
    role_choice_input = input(
"Choisissez un nouveau rôle en rentrant le numéro (laissez blanc pour passer) : ")
    role_id = roles[int(role_choice_input) - 1].id if role_choice_input else None

    return {
        "name": name,
        "email": email,
        "employee_number": employee_number,
        "role_id": role_id,
    }


def update_user_view(current_user, db=None):
    db = db or next(get_db())
    users = db.query(User).all()

    row_number = get_user_id_to_be_updated(users)
    user_to_update = users[int(row_number) - 1]
    
    roles_service = RoleService(db)
    roles = roles_service.get_all_roles()

    update_data = get_update_user_data(roles)

    users_service = UserService(db=db)
    updated_user = users_service.update_user(current_user, user_to_update.id, update_data)
    print(f"Utilisateur {updated_user.name} modifié avec succès")
    return current_user


def get_user_id_to_be_updated(users):
    print("\nQuel utilisateur voulez-vous modifiez ?")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.email}")

    row_number = input("Entrez le numéro de ligne : ")
    return int(row_number)


def get_user_id_to_be_deleted(users: list[User]):
    print("\nQuel utilisateur voulez-vous supprimez ?")
    for i, user in enumerate(users, start=1):
        print(f"{i}. {user.email}")

    row_number = input("Entrez le numéro de ligne : ")
    return int(row_number)


def delete_user_view(current_user, db=None):
    db = db or next(get_db())
    users = db.query(User).all()

    row_number = get_user_id_to_be_deleted(users)
    user_to_delete = users[int(row_number) - 1]
    users_service = UserService(db=db)
    users_service.delete_user(current_user, user_id=user_to_delete.id)
    print(f"User : {user_to_delete.id} | {user_to_delete.name} deleted")
