import logging
import random

from fastapi import APIRouter, HTTPException, status
from schemas import Number, NumbersToSum, Result

router = APIRouter(prefix="/numbers", tags=["Numbers"])


@router.get("/", status_code=status.HTTP_200_OK, summary="Get a number, or not!")
def get() -> Number:
    if random.randint(1, 3) == 1:  # 33,33% chance of true
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Ops, internal error!")

    return Number(number=random.randint(1, 100))


@router.post("/", status_code=status.HTTP_200_OK, summary="Sum two numbers")
def post(request: NumbersToSum) -> Result:
    return Result(result=request.number1 + request.number2)
