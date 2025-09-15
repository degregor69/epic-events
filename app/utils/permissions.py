from functools import wraps


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
        user = kwargs.get("user") or args[0]
        if not user or user.role.name != "sales":
            raise Exception("Accès refusé (réservé aux Sales)")
        return func(*args, **kwargs)

    return wrapper


def is_support(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = kwargs.get("user") or args[0]
        if not user or user.role.name != "support":
            raise Exception("Accès refusé (réservé au Support)")
        return func(*args, **kwargs)

    return wrapper
