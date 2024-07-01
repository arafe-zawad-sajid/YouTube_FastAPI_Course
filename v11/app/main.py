#run: "uvicorn v10.main:app" and append: "--reload" for auto reload

#--- Database Migration ---#
#Currently whenever we want to change our table properties we have to 
#drop the table and create it again, this isn't ideal 
#We're going to use a tool called Alembic so that whenever we add a col
#in a table from our models.py it automatically updates the db 
#We'll manage our db using Alembic instead of doing it manually or using workarounds  
#It allows to create incremental changes and rollback our db models/tables/schemas
#like we do with out code using GIT
# alembic init dir_name
#We drop all tables, we have no tables defined
#We'll go through this step by step as if we knew about alembic from start
#We create a "posts" table, then "users" table,
#then we setup a relationship along with the necessary foreign keys
#then we create "votes" table and setup the necessary foreign keys for that as well
# alembic revision -m "message_comment" like git commit -m
#Revisions track all of the changes, we can find it under alembic\versions dir 
#We have to setup the upgrade() and downgrade() funcs manually in the revisions dir
# alembic upgrade revision_id
#This will create the "posts" table as well as a "alembic_version" table
#alembic uses the latter table to keep track of the revisions    
#We add a new col to "posts" table by creating a new revision
# alembic revision -m "add content column to posts table" 
#Again we put in the logic for upgrading and downgrading
# alembic current
# alembic heads
# alembic upgrade head OR alembic upgrade revision_id
# alembic downgrade -1 OR alembic downgrade revision_id 
# alembic revision -m "add users table"
# alembic history
# alembic upgrade +1 OR alembic upgrade revision_id
# alembic upgrade head
#This time we'll not manually create the "votes" table, we're gonna use the auto-generate feature
#alembic will take a look at all of our models and based on the cols we have set here,
#it'll figure out what the diff between our models and db and make necessary changes
# alembic revisions --autogernate -m "message_comment"
# alembic upgrade head 
# 

from fastapi import FastAPI
from . import models  #one dot means current dir
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


#setting up stuff
# models.Base.metadata.create_all(bind=engine)  #since we've alembic we don't need this
app = FastAPI()  #fastapi instance

app.include_router(post.router)  #importing the router obj from post.py
app.include_router(user.router)  #the request will go into user.py and look for the route
                                 #if it finds a match it will respond like it normally does
app.include_router(auth.router)
app.include_router(vote.router)

#path operation/route
@app.get("/")  #decorator
async def root():  #function
    return {"message": "welcome to my api"}  #sends this to the Get request


