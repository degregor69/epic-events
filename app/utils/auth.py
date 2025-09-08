from functools import wraps
from app.utils.security import (
    verify_access_token,
    refresh_tokens,
    load_tokens,
    save_tokens,
)


def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            tokens = load_tokens()
        except FileNotFoundError:
            raise Exception("Authentication failed")

        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")

        try:
            verify_access_token(access_token)
        except Exception:
            try:
                new_tokens = refresh_tokens(refresh_token)
                save_tokens(new_tokens)
                verify_access_token(new_tokens["access_token"])
            except Exception:
                raise Exception("Authentication failed")

        return func()

    return wrapper
