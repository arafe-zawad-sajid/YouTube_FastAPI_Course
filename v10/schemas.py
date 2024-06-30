from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

#--- User: Request Model ---#
class UserCreate(BaseModel):  #creating a user
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

#--- User: Response Model ---#
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:  #Config converts the orm model to pydantic model
        orm_mode=True

#--- Vote: Request Model ---#
# 
class Vote(BaseModel):
    post_id: int
    # dir: conint(le=1)
    dir: conint(ge=0, le=1)  #0<dir<1
                             #we could also use bool here instead
                             #we could also use Literal[0, 1]


#--- Post: Request Model ---#
#pydantic model/schema
#data is validated according to this schema
#this handles user data that is sent to us
class PostBase(BaseModel):
    title: str  #mandatory property
    content: str  #mandatorty property
    published: bool = True  #optional property
    # rating: Optional[int] = None  #fully optional field

class PostCreate(PostBase):  #extends PostBase and inherits it's fields
    pass

#--- Post: Response Model ---#
#this handles our data being sent to the user
class Post(PostBase):  #Post extends/inherits from PostBase
    id: int  #we only specify the new columns we want to add in the response
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode=True

#CHECK AGAIN
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode=True

#--- Token: Request Model ---#
#we define a schema for the token because the user has to provide the access token
#if we expect them to send sth it's best to setup a schema
class Token(BaseModel):
    access_token: str
    token_type: str

#we setup a schema for the token data that is embedded in our access token
#this will ensure that all the data we pass in the token is actually there
class TokenData(BaseModel):
    # id: Optional[str] = None  #CHECK THIS AGAIN
    id: Optional[int] = None  #we shouldn't make this optional



