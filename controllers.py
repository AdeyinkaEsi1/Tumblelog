from fastapi import *
from typing import Annotated
from mongoengine import *
from fastapi import *
from fastapi.security import *
from fastapi import HTTPException
from main import *
from schemas import *
from models import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI

class Controllers:
    async def root():
        return {"Hello THERE"}
    
# token: Annotated[str, Depends(oauth2_scheme)]
    async def list_users():
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
            # return {"token": token}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    
    async def delete_user(user_id: str):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return {"message": "User deleted successfully"}
        except DoesNotExist:
            raise HTTPException(status_code=500, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(f"{e}"))
        
    
    async def list_posts():
        posts = Post.objects.all()
        post_data = []
        for post in posts:
            author_data = UserResponseSchema(
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
            })
        return post_data
    

    async def create_post(post_data: CreatePostSchema):
        author_data = post_data.author
        author = User(first_name=author_data.first_name, last_name=author_data.last_name, email=author_data.email)
        author.save()  # Save the author to the database first

        post = Post(title=post_data.title, author=author, tags=post_data.tags)

        comments = []
        for comment_data in post_data.comments:
            if comment_data.content:
                comments.append(Comment(content=comment_data.content, name=comment_data.name))
        post.comments = comments
        post.save()

        return {"message": "Post created successfully"}

            
        