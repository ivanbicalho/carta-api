from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse

from schemas import Detail

router = APIRouter(tags=["Hello World"])


@router.get("/hello", status_code=status.HTTP_200_OK, response_class=PlainTextResponse, summary="Hello world")
def hello() -> str:
    return "Hello World!"


@router.get("/hey", status_code=status.HTTP_200_OK, summary="Hey")
def hey() -> Detail:
    return Detail(message="Hey!")
