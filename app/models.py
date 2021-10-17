from typing import List, Optional

from sqlmodel import SQLModel, Field,Relationship

# user


# base user schema


class BaseUser(SQLModel):
    name:str
    email: str


# user table in database
class User(BaseUser, table=True):
    id: Optional[int] = Field(None, primary_key=True)
    password: str
    videos: List["Video"] = Relationship(back_populates="user")

# user schema for signup input


class UserCreate(BaseUser):
    password: str

# user schea for response


class UserRead(BaseUser):
    id: Optional[int] = Field(None, primary_key=True)

# user schema for login input



# video

# video base schema


class VideoBase(SQLModel):
    title: str
    description: str


# video database model

class Video(VideoBase, table=True):
    id: Optional[int] = Field(None, primary_key=True)
    file_name: str
    content_type: str
    user: Optional[User] = Relationship(back_populates="videos")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    

# video create schema


class VideoRead(VideoBase):
    id: int
    file_name: str
    content_type: str
    user_id:int



class UserReadWithVideos(UserRead):
    videos:List[VideoRead] = []



class VideoReadWithUser(VideoRead):
    user:UserRead = None