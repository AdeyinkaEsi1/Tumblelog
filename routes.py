from mongoengine import *
from fastapi import *
from fastapi.security import *
from main import *
from schemas import *
from models import *
from controllers import Controllers


router = FastAPI()

router.get("/",
           status_code=status.HTTP_200_OK
           )(Controllers.root)



router.get("/users",
        response_model=List[UserSchema],
        status_code=status.HTTP_200_OK
        )(Controllers.list_users)


router.get("/user/{user_id}",
           status_code=status.HTTP_204_NO_CONTENT
           )(Controllers.delete_user)


router.get("/posts/", response_model=List[PostSchema],
           status_code=status.HTTP_200_OK,
           )(Controllers.list_posts)


router.post("/post/new",
          status_code=status.HTTP_201_CREATED,
          )(Controllers.create_post)
