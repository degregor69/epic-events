import pytest
from unittest.mock import patch

from app.services.users import UserService
from app.views.users import create_user_view
from app.models import User


def test_management_login_and_create_user(db, management_user, roles):
    user_service = UserService(db=db)

    with patch("app.utils.security.create_access_token") as mock_access, patch(
        "app.utils.security.create_refresh_token"
    ) as mock_refresh, patch("app.utils.security.save_tokens") as mock_save, patch(
        "app.views.users.get_create_user_data"
    ) as mock_get_create_data:

        mock_access.return_value = "access.token"
        mock_refresh.return_value = "refresh.token"

        success, message, user = user_service.login_user(
            management_user.email, "test123?"
        )

        assert success is True
        assert message == "Login successful"
   
        mock_get_create_data.return_value = {
            "name": "Integration Created",
            "email": "integration.created@example.com",
            "employee_number": 321,
            "role_id": roles[2].id,  # choose 'support' or any available
            "password": "integration-pass-1",
        }

        created_user = create_user_view(management_user, db=db)

        db_user = db.query(User).filter_by(email="integration.created@example.com").first()
        assert db_user is not None
        assert db_user.email == "integration.created@example.com" == created_user.email
        assert db_user.hashed_password != "integration-pass-1"
