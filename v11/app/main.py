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
#--- CORS Policy ---#
#Till now we've been testing our API by sending requests from Postman
#here we actually send the request from our own pc 
#but in the reality our API can get requests from diff kinds of devices
#we can get requests from a pc/server through Postman or even CURL
#Postman does the same thing as CURL but has a nice GUI
#We can also get requests from mobiles/web browsers   
#When a web browser sends a request using JavaScript's fetch API, 
#there's gonna be slightly diff behavior that we must account for
#which we can't take into consideration while using Postman because it's not a web browser
#Now we're gonna send a API request (run the app) from Google Chrome's inspect element > console
# fetch('http://localhost:8000').then(res => res.json()).then(console.log) 
#This sends a request to the root URL of our API and print whatever the server returns
#But we get an error that it's blocked by CORS policy whereas in Postman it works fine
#CORS (Cross Origin Resource Sharing), this policy allows us to make a request from
#a web browser on one domain to a server on a diff domain 
#When we configure an API through any framework/language, by default we are only
#able to send requests from a web browser running on the same exact domain as the server
#If our API is hosted on Google and website on Ebay, be default 
#Ebay can't send a request to an API running on a diff domain like Google
#CORS will block it. But if our website also runs on Google 
#then by default they'd be able to talk just fine  
#Now if we try to send a request to our API URL from our browser it'll work
#it's same as sending a API request from the browser's console like before
#This works because the website is in the same domain/URL as the API server
#If we want to allow people from other domains to talk to our API look at the documentation > CORS
#We use corsmiddleware to allow specific domains like Google
#but if we try from a diff domain like Youtube and send the same exact request
#from the browser's dev console, it'll give error     
#If we want to allow Youtube we just add it to our list of allowed origins 
# 
#--- GIT ---#
#Firstly create .gitignore file in root folder of the project, don't upload pycache, virtual env, .env 
#Generate "requirements.txt" to list all the packages and libraries we need to install
# pip freeze > requirements.txt
#If anyone clones our repo they need to install the dependencies based on the file
# pip install -r requirements.txt
#Install GIT, def branch name should be main
#need an account on github and create a new repo 
#initialize git in root folder of our project
# git init
# git add --all  
# git commit -m "initial commit"
#Gives us an error, tells us to setup our user for our account on this machine
# git config --global user.email azs@gmail.com 
# git config --global user.name azs
# git commit -m "initial commit" 
#Set what our branch is
# git branch -M main
#We've to setu a remote branch, we name it origin here
# git remote add origin https://github.com/arafe-zawad-sajid/FastAPI_Project 
#Finally we need to do a git push
# git push -u origin main  
#A popup asks us to sign in and authorize
#  
#--- Application Deployment (Heroku) ---#
#This is the first of two deployment methods we're gonna learn in this course
#We're gonna deploy the app to a platform called Heroku so we need an account 
#It made it very easy to deploy the app and push out changes to the app
#After we create a Heroku account, we need to setup git which we've already done
#Now we setup Heroku (CLI) itself 
# heroku create fastapi-sajid
# git remote
#now we have two remotes, origin and heroku, the latter was added by heroku
# git push heroku main
#It'll push our code to heroku platform and then it'll create an instance for our app
#After it's done it'll give us a URL of our app in the log which we open up in the browser
#It'll fail because heroku doesn't know how to start up our app, it just knows it's a python app
#In our dev env we ran the app using uvicorn
# uvicorn app.main:app
#We actually have to create a Procfile file in the root dir that tells heroku what commands to run  
#Now we have to push out these changes to git
# git add -all
# git commit -m "added Procfile" 
# git push origin main
#Now we push out these changes to heroku to run our app
# git push heroku main
#Go to the heroku URL and refresh, but there are still issues, let's check the logs
# heroku logs -t
#From logs we can see that there are some issues with settings (the pydantic model for retrieving our env vars) 
#It's saying that there are a couple of validation errors for our settings model
#It's saying we don't have a db host name, db port, other infos.
#That's because, in dev we use our ".env" file to provide all our env vars into that settings model
#we specified that in Config where we set ".env" as our env_file
#In git, we didn't push our ".env" file, we excluded that in ".gitignore" file
#Now, we have to add those env vars through the cmd line or the dashboard 
#We also need a postgres db file, heroku provides us with a free postgres instance 
# heroku addons: create heroku-postgresql: hobby-dev
#      

from fastapi import FastAPI
from . import models  #one dot means current dir
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware  #to handle CORS policy


#setting up stuff
# models.Base.metadata.create_all(bind=engine)  #since we've alembic we don't need this
app = FastAPI()  #fastapi instance

# origins = ["https://www.google.com", "http://www.youtube.com"]  #list of domains that can talk to our API
origins = ["*"]  #for a public API we allow all domains

#middleware is a term used in web frameworks, it's basically a func that runs before every request
#If someone sends a request to our app, before it goes through the routers 
#it'll actually go through the middleware which will perform some kind of operations
#CORS policy can be very granular, not only we can allow specific domains
#we can also allow specific http methods
#If we build a public API where people can just retrieve data
#we may not want them to send POST, PUT, DELETE requests, we'll only allow GET requests     
#We can even allow specific headers as well
#  
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  #what domains should be able to talk to our API
    allow_credentials=True,
    allow_methods=["*"],  #allowing all methods
    allow_headers=["*"]  #allowing all headers
)

app.include_router(post.router)  #importing the router obj from post.py
app.include_router(user.router)  #the request will go into user.py and look for the route
                                 #if it finds a match it will respond like it normally does
app.include_router(auth.router)
app.include_router(vote.router)

#path operation/route
@app.get("/")  #decorator
async def root():  #function
    return {"message": "welcome to my api"}  #sends this to the Get request


