#run: "uvicorn v10.main:app" and append: "--reload" for auto reload

#--- Database Migration ---#
#Currently whenever we want to change our table properties we have to 
#drop the table and create it again, this isn't ideal 
#We're going to use a tool called Alembic so that whenever we add a col
#in a table from our models.py it automatically updates the db 
#We'll manage our db using Alembic instead of doing it manually or using workarounds  
#It allows to create incremental changes and rollback our db models/tables/schemas
#like we do with out code using GIT
# 

from fastapi import FastAPI
from . import models  #one dot means current dir
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


#setting up stuff
models.Base.metadata.create_all(bind=engine)  #creates db tables
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


