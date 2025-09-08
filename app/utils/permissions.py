from functools import wraps


def is_management(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("user") or args[0]
        if not user or user.role.name != "management":
            print("❌ Accès refusé (réservé au Management)")
            return
        return func(*args, **kwargs)

    return wrapper


def is_sales(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("user") or args[0]
        if not user or user.role.name != "sales":
            print("❌ Accès refusé (réservé aux Sales)")
            return
        return func(*args, **kwargs)

    return wrapper


def is_support(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("user") or args[0]
        if not user or user.role.name != "support":
            print("❌ Accès refusé (réservé au Support)")
            return
        return func(*args, **kwargs)

    return wrapper
