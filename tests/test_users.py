import pytest
from faker import Faker
from app.services.users import UserService
from app.models import User
from app.utils.auth import is_authenticated
from app.utils.security import (
    create_access_token,
    save_tokens,
    load_tokens,
    verify_access_token,
    create_refresh_token,
)
from unittest.mock import patch

from app.views.users import create_user_view, update_user_view, delete_user_view

fake = Faker()
TOKEN_FILE = "token.json"


def test_expired_access_and_refresh():
    with patch("app.utils.auth.load_tokens") as mock_load:
        mock_load.return_value = {
            "access_token": "expired",
            "refresh_token": "expired",
        }

        @is_authenticated
        def secret_action():
            return "secret!"

        with pytest.raises(Exception, match="Authentication failed"):
            secret_action()


def test_authentication_flow(db, support_user):
    access_token = create_access_token(support_user.email)
    refresh_token = create_refresh_token(support_user.email)
    save_tokens({"access_token": access_token, "refresh_token": refresh_token})

    tokens = load_tokens()
    assert "access_token" in tokens
    payload = verify_access_token(tokens["access_token"])
    assert payload["sub"] == support_user.email

    @is_authenticated
    def secret_action():
        return "secret!"

    assert secret_action() == "secret!"


def test_create_user(db, roles, management_user):
    selected_role = roles[1]
    password = fake.pystr(min_chars=12, max_chars=12)
    user_service = UserService(db=db)
    user = user_service.create_user(
        current_user=management_user,
        name="Test User",
        email="test_user@test.com",
        password=password,
        role_id=selected_role.id,
        employee_number=fake.pyint(min_value=100, max_value=200),
    )
    assert user.id is not None

    db_user = db.query(User).filter_by(email="test_user@test.com").first()
    assert db_user is not None
    assert db_user.hashed_password != password


def test_create_user_view_success(db, management_user):
    with patch("app.views.users.get_create_user_data") as mock_get_create_user_data:
        mock_get_create_user_data.return_value = {
            "name": "John Doe",
            "email": "john@example.com",
            "employee_number": 42,
            "role_id": 1,
            "password": "password123",
        }

        user = create_user_view(management_user, db)

    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert user.employee_number == 42
    assert user.role_id == 1


def test_update_user_view_success(db, support_user, roles, management_user):
    with patch("app.views.users.get_update_user_data") as mock_get_update_user_data, patch("app.views.users.get_user_id_to_be_updated") as mock_get_user_id_to_be_updated:
        mock_get_update_user_data.return_value = {
            "name": "New name",
            "email": "new@email.com",
            "employee_number": 999,
            "role_id": roles[0].id,
        }
        mock_get_user_id_to_be_updated.return_value = 1
        updated_user = update_user_view(current_user=management_user, db=db)

        db.refresh(support_user)
        assert support_user.name == "New name"
        assert support_user.email == "new@email.com"
        assert support_user.employee_number == 999
        assert support_user.role_id == roles[0].id


def test_create_user_view_permission_denied(
    support_user,
    db,
):
    with pytest.raises(Exception) as exc:
        with patch("app.views.users.get_create_user_data") as mock_get_create_user_data:
            mock_get_create_user_data.return_value = {
                "name": "John Doe",
                "email": "john@example.com",
                "employee_number": 42,
                "role_id": 1,
                "password": "password123",
            }

            create_user_view(support_user, db=db)
            assert str(exc.value) == "Accès refusé (réservé au Management)"


def test_delete_user(management_user, db, user_to_be_deleted):
    with patch(
        "app.views.users.get_user_id_to_be_deleted"
    ) as mock_get_user_id_to_be_deleted:
        mock_get_user_id_to_be_deleted.return_value = user_to_be_deleted.id
        delete_user_view(management_user, db)

        deleted_user = db.get(User, user_to_be_deleted.id)
        assert deleted_user is None


def test_delete_user_view_permission_denied(
    support_user,
    db,
):
    with pytest.raises(Exception) as exc:
        with patch(
            "app.views.users.get_user_id_to_be_deleted"
        ) as mock_get_user_id_to_be_deleted:
            mock_get_user_id_to_be_deleted.return_value = 1
            delete_user_view(support_user, db)
            assert str(exc.value) == "Accès refusé (réservé au Management)"


def test_login_user_not_found(db):
    user_service = UserService(db=db)

    success, message, user = user_service.login_user("noone@example.com", "pw")
    assert success is False
    assert message == "User not found"
    assert user is None


def test_login_user_wrong_password(db):
    from app.utils.security import hash_password

    # create a user with a hashed password so verify_password will run and fail for wrong pw
    user = db.query(User).filter_by(email="wrongpw@example.com").first()
    if not user:
        user = User(
            name="Wrong Pw",
            email="wrongpw@example.com",
            hashed_password=hash_password("rightpassword"),
            employee_number=456,
            role_id=None,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    user_service = UserService(db=db)

    success, message, returned_user = user_service.login_user(
        user.email, "incorrect")
    assert success is False
    assert message == "Wrong password"
    assert returned_user is None
