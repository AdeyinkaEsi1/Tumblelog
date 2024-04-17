from typing import List, Optional, Union
from pydantic import *


class UserSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class CreateUserSchema(UserSchema):
    password: str
    pass


class UserResponseSchema(UserSchema):
    id: str


class UpdateUserSchema(UserSchema):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class CommentSchema(BaseModel):
    name: str
    content: str


class CreatePostSchema(BaseModel):
    title: str
    author: UserSchema
    tags: List[str]
    comments: List[CommentSchema]
    # content: Optional[TextPostSchema]
    # image_path: Optional[ImagePostSchema]
    # link_url: Optional[LinkPostSchema]

class ListPostSchema(BaseModel):
    title: str
    author: UserResponseSchema
    tags: List[str]
    comments: List[CommentSchema]


class TextPostSchema(BaseModel):
    content: str


class LinkPostSchema(BaseModel):
    link_url: str


class ImagePostSchema(BaseModel):
    image_path: str