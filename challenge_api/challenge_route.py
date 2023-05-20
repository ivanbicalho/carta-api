from typing import List
from fastapi import APIRouter, HTTPException, status
from helpers import get_pass, get_story, get_vault, get_vault_names
from schemas import ChildFeedback, ChildStory, Vault

router = APIRouter(prefix="/challenge", tags=["Challenge"])


@router.get("/key", status_code=status.HTTP_200_OK, summary="Get the key to open the box")
def get_key():
    return {"key": get_pass("key")}


@router.get("/box", status_code=status.HTTP_200_OK, summary="Open the box and get the letter")
def box(box_key: str):
    if box_key != get_pass("key"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid box key")

    return get_story()


@router.post(
    "/child",
    status_code=status.HTTP_200_OK,
    summary="Get the child's feedback on the story you read to them",
)
def child(request: ChildStory) -> ChildFeedback:
    if not request.story:
        return ChildFeedback(feedback="What is the story? I can't hear you, please speak louder!")

    if request.story != get_story():
        return ChildFeedback(feedback="I don't like this story, please read me another one!")

    return ChildFeedback(
        feedback="I loved the story, thank you!! Let me whisper you the room code, don't share it!",
        room_code=get_pass("room"),
    )


@router.get("/room", status_code=status.HTTP_200_OK)
def get(room_code: str):
    if room_code != get_pass("room"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid room code")

    return [get_vault(name) for name in get_vault_names()]


@router.get("/vault", status_code=status.HTTP_200_OK)
def post(name: str, password: str) -> Vault:
    if name not in get_vault_names():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Vault not found")

    vault = get_vault(name)
    if password != vault.password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"Invalid password for {name}")

    return vault
