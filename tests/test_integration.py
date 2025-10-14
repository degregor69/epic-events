
import pytest
from unittest.mock import patch

from app.models.clients import Client
from app.models.events import Event
from app.services.clients import ClientService
from app.services.contracts import ContractService
from app.services.events import EventService
from app.services.users import UserService
from app.views.contracts import create_contract_view
from app.views.users import create_user_view
from app.models import User
from app.views.clients import create_client_view


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

def test_client_with_contract_and_create_an_event_and_updating_it(db, sales_user, management_user, support_user):

    # Sales user creates a new client
    clients_service = ClientService(db=db)
    created_client = clients_service.create_client(
        current_user=sales_user,
        full_name="Test User",
        email="test_user@example.com",
        phone="0123456789",
        company="Test Corp")
  


    db_client = db.query(Client).filter_by(email="test_user@example.com").first()
    assert db_client is not None
    assert db_client.id == created_client.id


    # Management user creates a contract for the new client
    contracts_service = ContractService(db=db)
    created_contract = contracts_service.create_contract(
        current_user=management_user,
        user_id=sales_user.id,
        client_id=created_client.id,
        total_amount=15000,
        pending_amount=5000,
        signed=True
    )
    assert created_contract.id is not None

    
    # Sales user can now create an event for that contract and client
    events_service = EventService(db=db)
    created_event = events_service.create_event(current_user=sales_user, 
                                                contract_id=created_contract.id,
                                                client_id=created_client.id,
                                                user_id=support_user.id,
                                                start_date="2025-12-31 10:00",
                                                end_date="2025-12-31 12:00",
                                                location="Test Location",
                                                attendees=100,
                                                notes="Test Notes")
    
    assert created_event is not None
    assert created_event.contract_id == created_contract.id
    assert created_event.client_id == created_client.id


    # Sales user updates the number of attendes of the event
    updated_event = events_service.update_event(
        current_user=sales_user,
        event_id=created_event.id,
        attendees=150
    )

    db_event = db.query(Event).filter_by(id=created_event.id).first()
    assert db_event is not None
    assert db_event.attendees == 150