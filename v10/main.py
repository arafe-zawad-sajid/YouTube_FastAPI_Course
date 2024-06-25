#run: "uvicorn v10.main:app" and append: "--reload" for auto reload

#--- Voting System ---#
#A user should be able to like a post once
#Anytime we retrieve the posts from our db/API we should also fetch the total no. of likes     
#We store the votes in another db table
#Every "post_id" and "user_id" pairs should be unique, we use composite keys here  
#It is just a primary key that spans multiple cols (instead of just 1) and ensures that accross those cols we have uniqne combinations
#Since a primary key must be unique, so we just make sure both the cols are part of the primary key 
#A composite primary key doesn't care if there are duplicates in any col, rather the col pairs
#In pgadmin, we just create "votes" table and set both "post_id" and "user_id" cols as primary keys
#We should setup two foreign keys for the two relationships, 
#one between posts and votes, another between users and votes 
#we make sure if a post or a user is deleted, it should cascade delete the related vote entries
#the foreign keys make sure we can't make an entry with non-existent user_id or post_id
#we need to setup the vote route in "routers\vote.py"
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


