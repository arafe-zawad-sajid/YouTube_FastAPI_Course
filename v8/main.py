#run: "uvicorn v8.main:app" and append: "--reload" for auto reload

#--- Database Relationships ---#
#For relational databases we setup relationships between tables
#We need to setup some kind of special relationship between users table 
#and posts table that will allow us to associate a post with a 
#specific user that created the post
#We do that by creating an extra col in our posts table called user_id
#We're going to setup a special foreign key
#A foreign key tells SQL that this col is connected to another table
#We specify the table (users) it should be connected to and which 
#Specific col (id col from users table) it should use from the table
#Whatever user creates this post, we just embed the id of that specific user
#One user can create many posts (one to many relationship)
#There'll be instances where you setup foreign keys to other cols 
#that aren't the id col, depending on how the relationships are setup 
#and how the app should work, it doesn't have to point to the id col of another table
#Data type of the cols should match
#If we don't provide user_id in posts, it'll give error
#if we provide user_id that doesn't exist, it'll give error
#If we delete a user who created one or more posts, it should delete 
#all the associated posts since we set cascade on delete
#Cascade delete means if parent is delete subsequent children will be deleted as well
#Eventually we'll look at SQL JOIN command that allows us to jam cols
#of multiple tables into one result, makes it easier to retrieve info
#We learned how to create and setup a foreign key using pgadmin,
#we're going to do this through code using sql alchemy, we update our models.Post  
#We also update schemas.Post but "create_post()" endpoint since owner_id was set as nullable=False
#We are not going to pass user_id to our schema, rather we'll retrieve it from the auth status 
#it's like when we create a post on twitter, twitter already knows the user_id
# 


from fastapi import FastAPI
from . import models  #one dot means current dir
from .database import engine
from .routers import post, user, auth


#setting up stuff
models.Base.metadata.create_all(bind=engine)  #creates db tables
app = FastAPI()  #fastapi instance

app.include_router(post.router)  #importing the router obj from post.py
app.include_router(user.router)  #the request will go into user.py and look for the route
                                 #if it finds a match it will respond like it normally does
app.include_router(auth.router)

#path operation/route
@app.get("/")  #decorator
async def root():  #function
    return {"message": "welcome to my api"}  #sends this to the Get request


