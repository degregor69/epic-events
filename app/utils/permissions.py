from functools import wraps

from app.models import Contract


def is_management(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("current_user") or args[0]
        if not user or user.role.name != "management":
            raise Exception("Accès refusé (réservé au Management)")
        return func(*args, **kwargs)

    return wrapper


def is_sales(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("current_user") or args[0]
        if not user or user.role.name != "sales":
            raise Exception("Accès refusé (réservé aux Sales)")
        return func(*args, **kwargs)

    return wrapper


def is_support(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("current_user") or args[0]
        if not user or user.role.name != "support":
            raise Exception("Accès refusé (réservé au Support)")
        return func(*args, **kwargs)

    return wrapper


def is_management_or_responsible_sales(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = kwargs.get("current_user") or args[0]
        contract_id = kwargs.get("contract_id") or args[1]
        contract = (
            kwargs.get("db").query(Contract).filter(Contract.id == contract_id).first()
        )

        if current_user.role.name == "management":
            return func(*args, **kwargs)

        if (
            current_user.role.name == "sales"
            and contract.client.internal_contact_id == current_user.id
        ):
            return func(*args, **kwargs)

        raise Exception("❌ Access denied")

    return wrapper
