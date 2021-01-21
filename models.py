from pydantic import typing
from pydantic.main import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: typing.Optional[str]
    content: typing.Optional[str]


class Post(BaseModel):
    id: int
    title: str
    content: str
