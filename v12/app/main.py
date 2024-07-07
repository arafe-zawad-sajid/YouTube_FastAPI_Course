#run: "uvicorn v10.main:app" and append: "--reload" for auto reload
 
#--- Application Deployment (Heroku) ---#
#Heroku is not free from 2022, it used to be, instead use Render
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
#It's saying we don't have a db host name, db port, and other infos.
#That's because, in dev we use our ".env" file to provide all our env vars into that settings model
#we specified that in Config where we set ".env" as our env_file
#In git, we didn't push our ".env" file, we excluded that in ".gitignore" file
#Now, we have to add those env vars through the cmd line or the dashboard 
#We also need a postgres db file, heroku provides us with a free postgres instance 
# heroku addons: create heroku-postgresql: hobby-dev
#If we refresh our dashboard we can see a new heroku instance, in its settings we can see our db credentials
#We can see the ip address in which the db lives on, heroku sets the db name which can't be changed
#we can see the username, port, password. They also provide us the whole postgres URL  
#Under settings we have Config Vars option where we provide env vars to our heroku instance
#Heroku calls our instance dynos 
#Heroku automatically added an env var called db URL. We can directly put it in "database.py" file
#But that would require us to change our code, so instead of using the default env var  
#we break down the URL into multiple env vars in heroku dyno settings as we did for orm 
#After setting up the env vars we restart heroku dyno
# heroku ps --help
# heroku ps restart
# heroku logs -t
#From logs we can see that we got a port assigned by heroku, this is why we provide the port variable
#However we don't need this port to access the app URL
# heroku apps: info fastapi-sajid
#we can find the Web URL for our app from here
#If we try to login through the documentation or postman, we'll get internal server error
#From logs we can see that we get some kind of SQL error, that's because the db is empty
#We can access our heroku postgres instance using pgAdmin
# open pgAdmin > create server > setup the connection   
#Now if we go into databases we'll see a lot of them because heroku provides one instance of db for free for multiple users
#The colored db is the one that we've access to
#We'll use alembic to create the tables since we've all our revisions setup
#In our dev env we used alembic to manage our db schema, alembic we responsible for creating the tables
# alembic upgrade head
#In our prod env we'll just run this cmd on our heroku instance
#Since our alembic folder is in git, heroku instance has access to it
#So when we run alembic, it can track all changes in our prod server as well
#But we never run alembic revision on our prod server, 
#we only run that on our dev server when we're staging out these changes
#In our prod server, when we want to stage our those changes we just do git push
#and push out the code changes and alembic revisions to git and subsequently our prod server
#Then we just run an alembic upgrade in our heroku instance, we don't add another line in Procfile though
# heroku run "alembic upgrade head"
#From logs we see that it has added in all the other incremental steps which can be later used to rollback
# heroku ps: restart
#Now we can see that everything is working, we've successfully deployed our app
#When we make changes to our code, we've to push out the changes to github and heroku
# git add --all
# git commit -m "new commit" 
# git push origin main
# git push heroku main
#When we make changes to our db, we've to create a new revision in alembic and push out the changes on heroku
# heroku run "alembic upgrade head"
#
#--- Application Deployment (Ubuntu Server) ---#
#We can host our ubuntu server on any major cloud providers like AWS, Azure, Digital Ocean, etc.
#We can also run it on our local machine with a virtual box, even on a raspberry pi
#The steps are going to be identical as long as we run it on an ubuntu server
#Select get started with a droplet, select ubuntu 20.04 (LTS) x64, basic, regular intel ssd
#Select closest data center, others default, authentication = password, hostname = ubuntu.fastapi
#Then we'll be given a public ip that we can use to connect to our VM   
#In windows, open terminal/cmd/vs code terminal, we use the ssh protocol
# ssh root@ip-address
#Select yes and put the password for the VM
# ls
#It'll show the content of our current dir, currently we've only one
# sudo apt update && sudo apt upgrade -y
#This will updated all of the installed packages 
#You can "keep the local version" or "install the package maintainer's version"
# python3 --version
#This will work, if we type only python it won't work
# sudo apt intall python3-pip
#We'll use pip to create a virtual env, we'll use it on this machine as well
# sudo pip3 install virtualenv  
#Now we install postgres 
# sudo apt install postgresql postgresql-contrib -y
#Before trying to connect it to our local machine, we'll connect from the ubuntu VM  
#CLI for accessing the postgres db
# psql --version
# psql -U postgres
#It'll give "peer auth error", it's not a usual log in failure 
#On ubuntu, postgres has a special way of authenticating users by def 
#When the ubuntu VM tries to connect to the db, it's called local auth
#Whereas, when we connect from our Windows machine to the postgres db on this ubuntu VM, that is peer auth
#Since we're on the same machine that we're trying to connect to our db, it is considered as local auth
#Peer auth is the def config for postgres, it takes the user that's logged in to the ubuntu machine
#and tries to log in as that user, in this case psql tries to log in as root user 
#It'll only allow a ubuntu user called postgres to be able to log in as the user called postgres on the postgres db in psql   
#It actually obtains the username from the linux kernel, so whoever you're logged in as is the only person you can log in as    
#We run this cmd to list out all the users 
# sudo cat /etc/passwd 
#We can see that a user called postgres was created on this machine, so we change our user
# su - postgres
# psql -U postgres
#We'll set up a password for this postgres suer
# \password postgres
#We exit out of the postgres console/terminal
# \q
#We're still logged in as the postgres user, we want to go back to the root user
# exit 
#To modify the configs for postgres, we want to move to a diff dir 
# cd /etc/postgresql/12/main
# ls
#We have to edit the files "postgresql.conf" and "pg_hba.conf"
# sudo vi postgresql.conf
#In the "Connections And Authentication" section we see that listen_address = 'localhost'
#That means, only if we're logged into this ubuntu VM we can connect to this postgres db 
#It'll not allow us to use pgAdmin from our Windows machine and connect to it remotely
#To be able to connect to it remotely we've to change these configs
# listen_addresses = *
#It'll allow me to connect from any ip address but in practice we should make it secure
# sudo vi pg_hba.conf 
#Now we change the configs under both local, edit peer > md5 for the two local method settings
#under the host settings, edit ip adress > 0.0.0.0/0 for ipv4 and ::/0 for ipv6
#When we change any config file we've to restart the app 
# systemctl restart postgresql
# psql -U postgres
#Enter the password and login
#Now we try to connect to it using pgAdmin on our Windows 
#Create server, go to general and set name = fastapi-prod 
#go to connection and set host name = ip address of our machine and provide password
#Generally on Ubuntu we shouldn't be logged in as root user, security risks  
#So we create another user with root priviledges
# adduser sajid
#We set the password
# su - sajid 
#Or we can exit out of root user and use ssh to directly log in as sajid
# ssh sajid@ip-address
#Enter the password   
#Any time we create a user we have to give sudo access in order to perform root priviledged operations
# usermod -aG sudo sajid  
#exit and connect back as user sajid 
# sudo apt upgrade
#Give password 
# pwd
#It gives us the dir we're in, default home is "/home/sajid" 
# cd ~
#It takes us to home dir 
#Now we create a folder for our app on our home dir
# mkdir app
# cd app
# virtualenv venv
#now we create a python venv like we did in the beginning of the tutorial 
# ls -la
#Now we activate the venv
# source venv/bin/activate  
#On the left side we see the venv activated
# deactivate
#This will deactivate the venv
# mkdir src
# cd src
# git clone github-clone-link .
#This will install our repo in our current dir (/app/src) 
# 
# 
# 
#   
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


