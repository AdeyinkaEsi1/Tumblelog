from typing import List
from pydantic import *


class UserSchema(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str


class CommentSchema(BaseModel):
    name: str
    content: str


class PostSchema(BaseModel):
    title: str
    author: UserSchema
    tags: List[str]
    comments: List[CommentSchema]
    # content: Optional[TextPostSchema]
    # image_path: Optional[ImagePostSchema]
    # link_url: Optional[LinkPostSchema]


class TextPostSchema(BaseModel):
    content: str


class LinkPostSchema(BaseModel):
    link_url: str


class ImagePostSchema(BaseModel):
    image_path: str