from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse

router = APIRouter(tags=["Hello World"])


@router.get("/hello", status_code=status.HTTP_200_OK, response_class=PlainTextResponse, summary="Hello world")
def hello():
    return "Hello World!"


@router.post("/hey", status_code=status.HTTP_200_OK, summary="Hey")
def hey():
    return {"message": "Hey!"}
