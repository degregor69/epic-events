import pytest

from app.services.clients import ClientService
from app.models import Client


def test_get_all_clients(db, clients):
    clients_service = ClientService(db=db)
    db_clients = clients_service.get_all_clients()

    assert len(db_clients) == len(clients)


def test_create_client(db, sales_user):
    client_data = {
        "full_name": "Alice Dupont",
        "email": "alice.dupont@example.com",
        "phone": "0123456789",
        "company": "ACME Corp",
    }

    clients_service = ClientService(db=db)
    created_client = clients_service.create_client(
        current_user=sales_user, **client_data
    )

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
    clients_service = ClientService(db=db)
    with pytest.raises(Exception) as exc:
        clients_service.create_client(support_user)
        assert str(exc.value) == "Accès refusé (réservé aux Sales )"


def test_update_client(db, sales_user, support_user, clients):
    client = clients[0]
    client.internal_contact_id = sales_user.id
    db.commit()
    clients_service = ClientService(db=db)

    updated_client = clients_service.update_client(
        current_user=sales_user,
        client_id=client.id,
        full_name="Alice Updated",
        email="alice.updated@example.com",
        phone="0987654321",
        company="Updated Corp",
        internal_contact_id=support_user.id,
    )

    assert updated_client is not None

    db_client: Client = db.get(Client, client.id)

    assert db_client.id == client.id
    assert db_client.full_name == "Alice Updated"
    assert db_client.email == "alice.updated@example.com"
    assert db_client.phone == "0987654321"
    assert db_client.company == "Updated Corp"
    assert db_client.internal_contact_id == support_user.id


def test_update_client_with_non_sales_user(db, sales_user, support_user, clients):
    client = clients[0]
    client.internal_contact_id = sales_user.id
    db.commit()
    clients_service = ClientService(db=db)

    with pytest.raises(Exception) as exc:
        updated_client = clients_service.update_client(
            current_user=support_user,
            client_id=client.id,
            full_name="Alice Updated",
            email="alice.updated@example.com",
            phone="0987654321",
            company="Updated Corp",
            internal_contact_id=support_user.id,
        )
        assert str(exc.value) == f"Client with id {client.id} not found"


def test_get_clients_by_user(db, sales_user, support_user, clients):
    clients[1].internal_contact_id = support_user.id
    db.commit()
    clients_service = ClientService(db=db)
    sales_user_clients = clients_service.get_clients_by_user(sales_user.id)
    assert len(sales_user_clients) == 1
    client = sales_user_clients[0]
    assert client.internal_contact_id == sales_user.id


def test_get_clients_with_signed_contracts(db, sales_user, clients, contracts):
    clients_service = ClientService(db=db)
    signed_clients = clients_service.get_clients_with_signed_contracts(
        sales_user.id)

    assert len(signed_clients) == 1

    client = signed_clients[0]

    assert client.id == clients[0].id
    assert any(contract.signed for contract in client.contracts)


def test_update_client_with_client_not_found(db, sales_user):
    clients_service = ClientService(db=db)

    with pytest.raises(Exception) as exc:
        clients_service.update_client(
            current_user=sales_user,
            client_id=999,
            full_name="new name",
            email="new_email@epic-events.com",
            phone="0000000000",
            company="New Company",
            internal_contact_id=sales_user.id)
        assert str(exc.value) == "Client with id 999 not found"
