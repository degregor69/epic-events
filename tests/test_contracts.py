import pytest

from app.services.contracts import ContractService
from app.models import Contract


def test_get_all_contracts(db, contracts):
    contracts_service = ContractService(db=db)
    db_contracts = contracts_service.get_all_contracts()

    assert len(db_contracts) == len(contracts)


def test_create_contract(db, management_user, contracts, clients):
    contracts_service = ContractService(db=db)
    created_contract = contracts_service.create_contract(
        current_user=management_user,
        user_id=management_user.id,
        client_id=clients[0].id,
        total_amount=5000,
        pending_amount=2000,
        signed=True,
    )

    assert created_contract is not None

    db_created_contract: Contract = db.get(Contract, created_contract.id)

    assert db_created_contract.id == created_contract.id
    assert db_created_contract.user_id == management_user.id
    assert db_created_contract.client_id == clients[0].id
    assert db_created_contract.total_amount == 5000
    assert db_created_contract.pending_amount == 2000
    assert db_created_contract.signed is True


def test_create_contract_with_non_authorized_user(
    db, support_user, management_user, contracts, clients
):
    with pytest.raises(Exception) as exc:
        contracts_service = ContractService(db=db)
        contracts_service.create_contract(support_user)
        assert str(exc.value) == "Accès refusé (réservé au Management)"


def test_update_contract(db, management_user, contracts, clients):
    contract = contracts[0]
    contracts_service = ContractService(db=db)
    updated_contract = contracts_service.update_contract(
        current_user=management_user,
        contract_id=contract.id,
        total_amount=7500,
        pending_amount=3500,
        signed=True,
        user_id=management_user.id,
        client_id=clients[1].id,
    )

    assert updated_contract is not None

    db_updated_contract: Contract = db.get(Contract, contract.id)

    assert db_updated_contract.id == contract.id
    assert db_updated_contract.total_amount == 7500
    assert db_updated_contract.pending_amount == 3500
    assert db_updated_contract.signed is True
    assert db_updated_contract.user_id == management_user.id
    assert db_updated_contract.client_id == clients[1].id


def test_update_contract_with_non_authorized_user(
    db, support_user, management_user, contracts, clients
):
    with pytest.raises(Exception) as exc:
        contracts_service = ContractService(db=db)
        contracts_service.update_contract(support_user)
        assert str(exc.value) == "Accès refusé (réservé au Management)"


def test_sales_update_contract(db, sales_user, contracts, clients, management_user):
    contract = contracts[0]
    contract.client.internal_contact_id = sales_user.id
    db.commit()

    contracts_service = ContractService(db=db)
    updated_contract = contracts_service.update_contract(
        current_user=sales_user,
        contract_id=contract.id,
        total_amount=8000,
        pending_amount=3000,
        signed=True,
        user_id=management_user.id,
        client_id=clients[1].id,
    )

    db_contract = db.get(Contract, contract.id)

    assert db_contract.id == contract.id
    assert db_contract.total_amount == 8000
    assert db_contract.pending_amount == 3000
    assert db_contract.signed is True
    assert db_contract.user_id == management_user.id
    assert db_contract.client_id == clients[1].id


def test_update_contract_with_contract_not_found(db, sales_user, contracts, clients):
    with pytest.raises(Exception) as exc:
        contracts_service = ContractService(db=db)
        contracts_service.update_contract(
            current_user=sales_user,
            contract_id=999,
            total_amount=8000,
            pending_amount=3000,
            signed=True,
            user_id=sales_user.id,
            client_id=clients[1].id,
        )
        assert str(exc.value) == "Contract with id 999 not found"


def test_get_all_contracts_for_user_clients(db, sales_user, contracts):
    contract = contracts[0]
    contract.client.internal_contact_id = sales_user.id
    db.commit()

    contracts_service = ContractService(db=db)
    db_contracts = contracts_service.get_all_contracts_for_user_clients(
        sales_user.id)

    assert len(db_contracts) == 2
    assert db_contracts[0].id == contract.id
    assert db_contracts[0].client.internal_contact_id == sales_user.id


def test_get_contracts_filtered_by_only_unsigned(db, contracts, sales_user):
    contracts_service = ContractService(db=db)
    filtered_contracts = contracts_service.get_contracts_filtered(
        current_user=sales_user, only_unsigned=True)

    assert len(filtered_contracts) == 1
    first_contract = filtered_contracts[0]
    assert first_contract.signed is False


def test_get_contracts_filtered_by_only_pending(db, contracts, sales_user):
    contracts_service = ContractService(db=db)
    filtered_contracts = contracts_service.get_contracts_filtered(
        current_user=sales_user, only_pending=True)

    assert len(filtered_contracts) == 2
    for contract in filtered_contracts:
        assert contract.pending_amount > 0
