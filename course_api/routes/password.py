import os

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyQuery

password_key = APIKeyQuery(name="password", auto_error=False)


def get_password(password: str, env_name: str) -> str:
    saved_password = os.getenv(env_name, None)
    if not saved_password:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Password not set")

    if password == saved_password:
        return password

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid password")


def password_to_get(password: str = Security(password_key)) -> str:
    return get_password(password, "PASSWORD_GET")


def password_to_post(password: str = Security(password_key)) -> str:
    return get_password(password, "PASSWORD_POST")


def password_to_delete(password: str = Security(password_key)) -> str:
    return get_password(password, "PASSWORD_DELETE")
