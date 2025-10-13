import jwt
import datetime
import os
import json
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_algorithm = os.getenv("JWT_ALGORITHM")
token_file = os.getenv("TOKEN_FILE")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(email: str, expires_delta: int = 3600) -> str:
    expire = datetime.datetime.now() + datetime.timedelta(seconds=expires_delta)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, jwt_secret_key, algorithm=jwt_algorithm)


def create_refresh_token(email: str, expires_delta: int = 604800) -> str:
    expire = datetime.datetime.now() + datetime.timedelta(seconds=expires_delta)
    payload = {"sub": email, "exp": expire, "type": "refresh"}
    return jwt.encode(payload, jwt_secret_key, algorithm=jwt_algorithm)


def verify_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            jwt_secret_key,
            algorithms=[jwt_algorithm],
            options={"verify_exp": True},
        )
    except jwt.ExpiredSignatureError:
        raise Exception("Access token expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid access token")


def verify_refresh_token(token: str) -> dict:
    payload = jwt.decode(
        token, jwt_secret_key, algorithms=[
            jwt_algorithm], options={"verify_exp": True}
    )
    if payload.get("type") != "refresh":
        raise Exception("Invalid refresh token")
    return payload


def refresh_tokens(refresh_token: str) -> dict:
    payload = verify_refresh_token(refresh_token)
    email = payload["sub"]
    new_access = create_access_token(email)
    new_refresh = create_refresh_token(email)
    return {"access_token": new_access, "refresh_token": new_refresh}


def save_tokens(tokens: dict, filename: str = token_file):
    with open(filename, "w") as f:
        json.dump(tokens, f)


def load_tokens(filename: str = token_file) -> dict:
    if not os.path.exists(filename):
        raise FileNotFoundError("No token.json found")
    with open(filename, "r") as f:
        return json.load(f)
