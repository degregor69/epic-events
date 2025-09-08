from functools import wraps


def is_management(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("user")
        if not user:
            user = args[0] if args else None

        if not user or user.role.name != "management":
            print("❌ Accès refusé : réservé aux managers")
            return

        return func(*args, **kwargs)

    return wrapper
