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


def can_update_event(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        current_user = kwargs.get("current_user") or args[1]
        event_id = kwargs.get("event_id") or args[2]

        if not current_user:
            raise Exception("current_user argument missing")

        event = self.event_db.get_by_id(event_id)
        if not event:
            raise Exception(f"Event {event_id} not found")

        if current_user.role.name == "support" and event.user_id != current_user.id:
            raise Exception("Access denied – not your event")

        return func(self, *args, **kwargs)

    return wrapper
