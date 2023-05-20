import os
from fastapi.security.api_key import APIKeyQuery
from fastapi import Security, HTTPException, status

password_key = APIKeyQuery(name="password", auto_error=False)

async def get_password(password: str = Security(password_key)) -> str:
    if password == os.getenv("PASSWORD"):
        return password
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid password"
    )

async def get_password2(password: str = Security(password_key)) -> str:
    if password == os.getenv("PASSWORD2"):
        return password
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid password"
    )