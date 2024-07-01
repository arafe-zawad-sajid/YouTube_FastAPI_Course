#SQL Alchemy models

from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

#SQL alchemy doesn't update table properties, we have to use a db migration tool like alembic
#For now we'll manually drop the post table and run the code to recreate it with the latest changes
#Since we added the foreign key, we have to update a few things to avoid errors
#We have to update our schema, else we won't see owner_id in our response when we retrieve posts
#   
class Post(Base):  #extends database.Base class
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)  #server_default not the same as default
    created_at = Column(TIMESTAMP(timezone=True), 
                        server_default=text('now()'), nullable=False)
    #foreign key
    owner_id = Column(Integer,
                      ForeignKey("users.id", ondelete="CASCADE"),
                      nullable=False)  #we must provide owner_id for every new post
    #setting up a relationship
    owner = relationship("User")  #referencing the SQL Alchemy class User, not the db table
                                  #it'll fetch the user based off of the owner_id and return the row 

    

#--- User Registration ---#
#users need to be able to create a brand new account
#we have to create a table within our db that's going to hold our user info
#we create a new orm model to define what our user table would look like
# 
class User(Base):  #extending database.Base is a requirement for any orm model
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        server_default=text('now()'), nullable=False)
    phone_number = Column(String)

#--- Voting System ---#
class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer,
                     ForeignKey("posts.id", ondelete="CASCADE"),
                     primary_key=True)
    user_id = Column(Integer, 
                     ForeignKey("users.id", ondelete="CASCADE"), 
                     primary_key=True)
