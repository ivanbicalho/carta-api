import os

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyQuery

password_key = APIKeyQuery(name="password", auto_error=False)


def get_password(password: str, env_name: str) -> str:
    if password == os.getenv(env_name):
        return password

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid password")


def password_to_get(password: str = Security(password_key)) -> str:
    return get_password(password, "PASSWORD_GET")


def password_to_post(password: str = Security(password_key)) -> str:
    return get_password(password, "PASSWORD_POST")


def password_to_delete(password: str = Security(password_key)) -> str:
    return get_password(password, "PASSWORD_DELETE")
