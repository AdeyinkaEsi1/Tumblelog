import json
from typing import List, Optional
from bson import ObjectId
from fastapi.responses import JSONResponse
from mongoengine import *
from fastapi import *
from pydantic import BaseModel, EmailStr
from uuid import uuid4, UUID

app = FastAPI()

connect("tumbledb")

class User(Document):
    email = EmailField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

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


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)

class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))

    meta = {"allow_inheritance": True}

class TextPost(Post):
    content = StringField()

class ImagePost(Post):
    image_path = StringField()

class LinkPost(Post):
    link_url = StringField()


# john = User(email='john@example.com', first_name='john', last_name='Lawley')
# john.save()
# ross = User(email='ross@example.com', first_name='Ross', last_name='Lawley')
# ross.save()

# post1 = TextPost(title='Fun with MongoEngine$', author=john)
# post1.content = 'Took a look at MongoEngine today, looks pretty cool.'
# post1.tags = ['mongodb', 'mongoengine']
# post1.save()

# post2 = LinkPost(title='MongoEngine Documentation$', author=ross)
# post2.link_url = 'http://docs.mongoengine.com/'
# post2.tags = ['mongoengine']
# post2.save()

# for post in Post.objects:
#     print(post.title)
# print()
# for post in TextPost.objects:
#     print(post.title)

# for post in Post.objects:
#     print(f'{post.title} \nAuthor --> {post.author.first_name} {post.author.last_name}' )
#     print('=' * len(post.title))

#     if isinstance(post, TextPost):
#         print( post.content)
#         print()

#     if isinstance(post, LinkPost):
#         print( 'Link:', post.link_url)
#         print()

#     print

@app.get("/")
async def root():
    return {"Hello THERE"}

from fastapi import HTTPException

@app.get("/users", response_model=List[UserSchema])
async def get_users():
    try:
        users = User.objects.all()
        user_data = []
        for user in users:
            user_data.append({
                "id": str(user.id),  # Convert ObjectId to string
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            })
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return {"message": "User deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=500, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(f"{e}"))



@app.get("/posts/", response_model=List[PostSchema])
async def get_posts():
    posts = Post.objects.all()
    post_data = []
    for post in posts:
        author_data = UserSchema(
            id=str(post.author.id),
            email=post.author.email,
            first_name=post.author.first_name,
            last_name=post.author.last_name
        )
        comments_data = []
        for comment in post.comments:
            comment_data = CommentSchema(
                content=comment.content,
                name=comment.name
            )
            comments_data.append(comment_data)
        post_data.append({
            "title": post.title,
            "author": author_data,
            "tags": post.tags,
            "comments": comments_data
        })
    return post_data
