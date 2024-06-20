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

class PostCreate(PostBase):  #extends PostBase and inherits it's fields
    pass



#--- Response Model ---#
#this handles our data being sent to the user
class Post(PostBase):  #Post extends/inherits from PostBase
    id: int  #we only specify the new columns we want to add in the response
    created_at: datetime

    class Config:
        orm_mode=True

