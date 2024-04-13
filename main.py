from typing import Annotated, List, Optional
from mongoengine import *
from fastapi import *
from pydantic import BaseModel
from fastapi.security import *
from fastapi import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)

class CommentSchema(BaseModel):
    name: str
    content: str


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))
    # content = ListField(EmbeddedDocumentField(TextPost))

    meta = {"allow_inheritance": True}


class TextPost(Post):
    content = StringField()

class TextPostSchema(BaseModel):
    content: str

class ImagePost(Post):
    image_path = StringField()

class ImagePostSchema(BaseModel):
    image_path: str

class LinkPost(Post):
    link_url = StringField()

class LinkPostSchema(BaseModel):
    link_url: str

class PostSchema(BaseModel):
    title: str
    author: UserSchema
    tags: List[str]
    comments: List[CommentSchema]
    # content: Optional[TextPostSchema]
    # image_path: Optional[ImagePostSchema]
    # link_url: Optional[LinkPostSchema]


@app.get("/")
async def root():
    return {"Hello THERE"}


@app.get("/users", response_model=List[UserSchema])
async def list_users(token: Annotated[str, Depends(oauth2_scheme)]):
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
        # return user_data
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/user/{user_id}")
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
async def list_posts():
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
        # for tpost in Post.objects:
        #     contents_data = []
        #     if isinstance(post, TextPost):
        #         content_data = TextPostSchema(content=tpost.content)
        #         contents_data.append(content_data)
        # elif isinstance(post, ImagePost):
        #     content_data = ImagePostSchema(image_path=post.image_path)
        # elif isinstance(post, LinkPost):
        #     content_data = LinkPostSchema(link_url=post.link_url)
        post_data.append({
            "title": post.title,
            "author": author_data,
            "tags": post.tags,
            "comments": comments_data,
            # "content": contents_data,
            # "image_path": content_data.image_path if isinstance(content_data, ImagePostSchema) else None,
            # "link_url": content_data.link_url if isinstance(content_data, LinkPostSchema) else None
        })
    return post_data


@app.post("/post/new")
async def create_post(post_data: PostSchema):
    # Convert Pydantic schema to MongoDB Document
    author_data = post_data.author
    author = User(first_name=author_data.first_name, last_name=author_data.last_name, email=author_data.email)
    author.save()  # Save the author to the database first

    # comment_data = post_data.comments
    # comments = [Comment(name=comment_data.)]

    post = Post(title=post_data.title, author=author, tags=post_data.tags)

    # Convert comment data
     # Convert comment data
    comments = []
    for comment_data in post_data.comments:
        # Check if comment text exists
        if comment_data.content:
            comments.append(Comment(content=comment_data.content, name=comment_data.name))
    post.comments = comments
    # comments = [Comment(content=comment.content) for comment in post_data.comments]
    # post.comments = comments

    # Save post to database
    post.save()

    return {"message": "Post created successfully"}





# =============================================

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
