#run: "uvicorn v6.main:app" and append: "--reload" for auto reload

#--- Using Routers ---#
#as we keep adding more path operations "main.py" file gets messier, we need to clean it up
#so we break it up and put them in seperate files
#the routes/path operations that deal with Posts will be in one file and vice versa
#we are not simply moving stuff around, we accomplish this using routers
#using routers we split up all of our path operations into diff files which helps us organize code better


from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas, utils  #one dot means current dir
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user

#setting up stuff
models.Base.metadata.create_all(bind=engine)  #creates db tables
app = FastAPI()  #fastapi instance

app.include_router(post.router)  #importing the router obj from post.py
app.include_router(user.router)  #the request will go into user.py and look for the route
                                 #if it finds a match it will respond like it normally does


#path operation/route
@app.get("/")  #decorator
async def root():  #function
    return {"message": "welcome to my api"}  #sends this to the Get request



