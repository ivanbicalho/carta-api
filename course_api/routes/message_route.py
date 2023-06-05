import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.api_key import APIKey
from schemas import Detail
from routes.password import password_to_delete, password_to_get, password_to_post
from schemas import Message

router = APIRouter(prefix="/messages", tags=["Messages"])

MESSAGES: List[Message] = []


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": List[Message]},
        status.HTTP_401_UNAUTHORIZED: {"model": Detail},
    },
    summary="List all messages",
)
def get(password: APIKey = Depends(password_to_get)) -> List[Message]:
    return MESSAGES


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": Message},
        status.HTTP_401_UNAUTHORIZED: {"model": Detail},
    },
    summary="Add a new message",
)
def post(message: Message, password: APIKey = Depends(password_to_post)) -> Message:
    if len(MESSAGES) >= 500:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Hum, sorry! Too many received messages, need to clean up first!"
        )

    MESSAGES.append(message)

    return message


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_401_UNAUTHORIZED: {"model": Detail},
    },
    summary="Clear all messages",
)
def delete(password: APIKey = Depends(password_to_delete)) -> None:
    MESSAGES.clear()
