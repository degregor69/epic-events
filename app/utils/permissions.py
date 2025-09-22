from functools import wraps

from app.models import Contract


def is_management(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(args)
        print(kwargs)
        current_user = kwargs.get("current_user") or (args[1] if args else None)

        print("🔹 current_user:", current_user)
        if not current_user:
            raise Exception("current_user argument missing")

        if current_user.role.name != "management":
            raise Exception("❌ Access denied")

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
    def wrapper(self, *args, **kwargs):
        current_user = kwargs.get("current_user") or (args[0] if args else None)
        contract_id = kwargs.get("contract_id") or (args[1] if len(args) > 1 else None)

        if not current_user or contract_id is None:
            raise Exception("Missing required arguments")

        db = getattr(self.contract_db, "db", None)
        if db is None:
            raise Exception("DB session not found in the service")

        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise Exception("Contract not found")

        if current_user.role.name == "management":
            return func(self, *args, **kwargs)

        if (
            current_user.role.name == "sales"
            and contract.client.internal_contact_id == current_user.id
        ):
            return func(self, *args, **kwargs)

        raise Exception("❌ Access denied")

    return wrapper
