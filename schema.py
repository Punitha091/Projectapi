from pydantic.types import conint
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class post(BaseModel):
    title: str
    content: str
    published: bool = True


class posts(BaseModel):
    id:int
    title: str
    content: str
    published: bool = True
    class Config:
        orm_mode=True


class userlogin(BaseModel):
    id:int
    email:str
    password:str

    class Config:
        orm_mode = True

class Post(posts):
    id:int
    created_at:datetime
    owner_id:int
    owner: userlogin

    class Config:
        orm_mode = True

  
class userdata(BaseModel):
    pass


class users(BaseModel):
    id:int
    username: str
    email: str
    password: str
    title: str
    content: str
    published: bool = True
    

    class Config:
        orm_mode = True
 

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)

