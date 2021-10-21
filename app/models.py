from typing import List, Optional

from sqlmodel import SQLModel, Field,Relationship

from datetime import datetime

class UserVideoLikesLink(SQLModel,table=True):
    user_id: Optional[int] = Field(None, primary_key=True,foreign_key="user.id")
    video_id: Optional[int] = Field(None, primary_key=True,foreign_key="video.id")


# user


# base user schema


class UserBase(SQLModel):
    name:str
    email: str


# user table in database
class User(UserBase, table=True):
    id: Optional[int] = Field(None, primary_key=True)
    password: str
    videos: List["Video"] = Relationship(back_populates="user")
    created_at:datetime = Field(default=datetime.utcnow())
    video_likes:List["Video"] = Relationship(back_populates="user_likes",link_model=UserVideoLikesLink)

# user schema for signup input


class UserCreate(UserBase):
    password: str


# user schea for response


class UserRead(UserBase):
    id: Optional[int] = Field(None, primary_key=True)
    created_at:datetime


# user schema for update 

class UserUpdate(SQLModel):
    name:Optional[str] = None
    email:Optional[str] = None
    

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
    views:int = Field(default=0)
    created_at:datetime = Field(default=datetime.utcnow())
    user_likes:List["User"] = Relationship(back_populates="video_likes",link_model=UserVideoLikesLink)


    

# video create schema


class VideoRead(VideoBase):
    id: int
    file_name: str
    content_type: str
    user_id:int
    views:int
    created_at:datetime




class UserReadWithVideos(UserRead):
    videos:List[VideoRead] = []



class VideoReadWithUser(VideoRead):
    user:UserRead = None




