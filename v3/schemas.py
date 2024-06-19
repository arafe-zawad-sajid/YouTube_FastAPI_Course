from pydantic import BaseModel
from datetime import datetime


#--- Request Model ---#
#pydantic model/schema
#data is validated according to this schema
class PostBase(BaseModel):
    title: str  #mandatory property
    content: str  #mandatorty property
    published: bool = True  #optional property
    # rating: Optional[int] = None  #fully optional field

class PostCreate(PostBase):
    pass

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool


#diff models for diff requests
#suppose we don't want the user to update the whole post rather a property
#not allowing them to provide any other fields



#--- Response Model ---#
class Post(PostBase):  #Post extends/inherits from PostBase
    id: int
    created_at: datetime
#the pydantic class takes a dict and compares it with a specific model
#by def the pydantic model is expecting a dict
#but new_post is a orm/sql alchemy model, but pydantic only knows how to work with dict
#so we have to tell it to convert this orm model to pydantic model
    class Config:
        orm_mode=True

