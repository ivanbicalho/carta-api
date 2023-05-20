from pydantic import BaseModel


class Message(BaseModel):
    name: str
    message: str


class Number(BaseModel):
    number: int


class NumbersToSum(BaseModel):
    number1: int
    number2: int


class Result(BaseModel):
    result: int
