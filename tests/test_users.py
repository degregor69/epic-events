import pytest
from faker import Faker
from app.controllers.users import create_user
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

from app.views.users import create_user_view

fake = Faker()
TOKEN_FILE = "token.json"


def test_create_user(db, roles):
    selected_role = roles[1]
    password = fake.pystr(min_chars=12, max_chars=12)
    user = create_user(
        db=db,
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
            print(Exception)
            secret_action()


def test_create_user_view_permission_denied(
    support_user,
    db,
):
    with pytest.raises(Exception) as exc:
        create_user_view(support_user)
        assert str(exc.value) == "Accès refusé (réservé au Management)"


def test_create_user_view_success(db, management_user):
    inputs = iter(
        [
            "John Doe",
            "john@example.com",
            "42",
            "1",
            "password123",
        ]
    )

    with patch("builtins.input", lambda _: next(inputs)):
        create_user_view(management_user)

    created = db.query(User).filter_by(email="john@example.com").first()
    assert created is not None
