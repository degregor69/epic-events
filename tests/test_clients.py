import pytest

from app.controllers.clients import get_all_clients, create_client
from app.models import Client


def test_get_all_clients(db, clients):
    db_clients = get_all_clients(db)

    assert len(db_clients) == len(clients)


def test_create_client(db, sales_user):
    client_data = {
        "full_name": "Alice Dupont",
        "email": "alice.dupont@example.com",
        "phone": "0123456789",
        "company": "ACME Corp",
    }

    created_client = create_client(current_user=sales_user, db=db, **client_data)

    assert created_client is not None

    db_client: Client = db.get(Client, created_client.id)

    assert db_client.id == created_client.id
    assert db_client.full_name == client_data["full_name"]
    assert db_client.email == client_data["email"]
    assert db_client.phone == client_data["phone"]
    assert db_client.company == client_data["company"]
    assert db_client.internal_contact_id == sales_user.id


def test_create_client_with_non_authorized_user(
    db, support_user, management_user, contracts, clients
):
    with pytest.raises(Exception) as exc:
        create_client(support_user)
        assert str(exc.value) == "Accès refusé (réservé aux Sales )"
