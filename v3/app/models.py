#this sql alchemy model defines how our db tables look like
#when using orm, we don't have to create our tables from pgadmin util
#we can define it as a python model
#whenever we start our app, sql alchemy will check for a table named "posts"
#if it's there it won't do anything, otherwise it'll create it for us based on what we defined in the model
#sql alchemy will generate a table only if one does not exist, it does not modify the tables
#for migrations (changing the cols and the schema) we use alembic, sql alchemy isn't meant for this



from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):  #extends database.Base class
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)  #"server_default" not the same as "default"
    created_at = Column(TIMESTAMP(timezone=True), 
                        server_default=text('now()'), nullable=False)  #server_default='now()' doesn't work as intended