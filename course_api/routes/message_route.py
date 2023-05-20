import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.api_key import APIKey
from routes.password import get_password, get_password2
from schemas import Message

router = APIRouter(prefix="/messages", tags=["Messages"])

MESSAGES: List[Message] = []


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Message], summary="List all messages")
def get() -> List[Message]:
    return MESSAGES


@router.post("/", status_code=status.HTTP_200_OK, response_model=Message, summary="Add a new message")
def post(message: Message, password: APIKey = Depends(get_password)) -> Message:
    if len(MESSAGES) >= 500:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Too many received messages")

    MESSAGES.append(message)

    return message


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, summary="Clear all messages")
def delete(password: APIKey = Depends(get_password2)) -> None:
    MESSAGES.clear()
