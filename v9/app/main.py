#run: "uvicorn v9.app.main:app" and append: "--reload" for auto reload

#--- Environment Variables ---#
#In a production env, we need a way for our code to auto update and point to the actual production db 
#Any kind of confidential info or anything that needs to be updated based off of the env that it's in
#We will make use of Environment Variables
#When we configure this in our computer any app that's running will be able to access it
#The python app will be able to access any env var on the machine  
#Instead of hardcoding the actual values we hardcode just the name of the env var
#and python will automatically retrieve the necessary env var
#On windows, under env vars we have system vars that are system wide
#and we have user vars that only a certain user can access   
#to access it, we run echo %var-name% on cmd, with python we use os.getenv("var-name")
#if we add a new env var on windows, to access it on cmd we have to re-open a new cmd
#to access it on vs code, we have to restart vs code  
#If we forget to setup a necessary env var our app may crash (since it's a dependency)
#Performing a validation to make sure the env vars have been set for the app is a good idea
#env var is always return a string, we have to do validation for that in code  
#In our schemas, we use pydantic to make sure that we have all our properties and to perform the typecasting (data validation)
#We can do the same for our env vars using pydantic
#When we move to production we can just set all the values inside our "config.py" file on our machine
#it's going to automatically import and update those values where ever we reference them
#      

from fastapi import FastAPI
from . import models  #one dot means current dir
from .database import engine
from .routers import post, user, auth
from .config import settings


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


