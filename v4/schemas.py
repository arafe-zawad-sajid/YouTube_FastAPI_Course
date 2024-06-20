from pydantic import BaseModel
from datetime import datetime


#--- Request Model ---#
#pydantic model/schema
#data is validated according to this schema
#this handles user data that is sent to us
class PostBase(BaseModel):
    title: str  #mandatory property
    content: str  #mandatorty property
    published: bool = True  #optional property
    # rating: Optional[int] = None  #fully optional field

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

class PostCreate(PostBase):  #extends PostBase and inherits it's fields
    pass

#updating and creating is fundamentally the same so we have just one



#--- Response Model ---#
#this handles our data being sent to the user
# class Post(BaseModel):  #Post extends/inherits from PostBase
#     title: str
#     content: str
#     published: bool
# 
# #the pydantic class takes a dict and compares it with a specific model
# #by def the pydantic model is expecting a dict
# #but new_post is a orm/sql alchemy model, but pydantic only knows how to work with dict
# #so we have to tell it to convert this orm model to pydantic model
#     class Config:
#         orm_mode=True

#this is how we define the data that is sent back by specifiying the fields we want to send
#with APIs we should explicitly define the data we want to send and receive
class Post(PostBase):  #Post extends/inherits from PostBase
    id: int  #we only specify the new columns we want to add in the response
    created_at: datetime

    class Config:
        orm_mode=True

