from typing import Optional
from pydantic import BaseModel


class ChildStory(BaseModel):
    story: str


class ChildFeedback(BaseModel):
    feedback: str
    room_code: Optional[str] = None


class Vault(BaseModel):
    name: str
    password: str
    content: str
