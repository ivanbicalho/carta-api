from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import PlainTextResponse
from helpers import get_pass, get_story, get_vault, get_vault_content, get_vault_names
from schemas import BoxKey, ChildFeedback, ChildStory, Vault, VaultContent

router = APIRouter(prefix="/challenge", tags=["Challenge"])


@router.get("/key", status_code=status.HTTP_200_OK, response_model=BoxKey, summary="Get the key to open the box")
def get_key() -> BoxKey:
    return BoxKey(key=get_pass("key"))


@router.get(
    "/box",
    status_code=status.HTTP_200_OK,
    response_class=PlainTextResponse,
    summary="Open the box and get the letter with the story",
)
def box(box_key: str) -> str:
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


@router.get(
    "/room",
    status_code=status.HTTP_200_OK,
    response_model=List[Vault],
    summary="Get all the vaults in the room and its passwords",
)
def get(room_code: str) -> List[Vault]:
    if room_code != get_pass("room"):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid room code")

    return [get_vault(name) for name in get_vault_names()]


@router.post(
    "/vault", status_code=status.HTTP_200_OK, response_model=VaultContent, summary="Open the vault and get its content"
)
def post(credentials: Vault) -> VaultContent:
    if credentials.name not in get_vault_names():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Vault not found")

    vault = get_vault_content(credentials.name)
    if credentials.password != vault.password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, f"Invalid password for {credentials.name}")

    return vault
