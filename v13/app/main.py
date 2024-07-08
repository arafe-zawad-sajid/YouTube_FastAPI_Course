#run: "uvicorn v10.main:app" and append: "--reload" for auto reload
 
#--- Application Deployment (Ubuntu Server) ---#
#We can host our ubuntu server on any major cloud providers like AWS, Azure, Digital Ocean, etc.
#We can also run it on our local machine with a virtual box, even on a raspberry pi
#The steps are going to be identical as long as we run it on an ubuntu server
#Select get started with a droplet, select ubuntu 20.04 (LTS) x64, basic, regular intel ssd
#Select closest data center, others default, authentication = password, hostname = ubuntu.fastapi
#Then we'll be given a public "ip-address" that we can use to connect to our VM   
#In windows, open terminal/cmd/vs code terminal, it's all the same
#To connect to a device, we use the ssh protocol
#In digital ocean, they create a root user for us
# ssh root@ip-address
#Select yes and put the password for the VM
# ls
#It'll show the content of our current dir, currently we've only one
#First thing to do is to updated all of the installed packages  
# sudo apt update && sudo apt upgrade -y
#You can "keep the local version" or "install the package maintainer's version", we select maintainer's version
# python3 --version
#This will work, but if we type only python it won't work
#We install pip if we don't have it installed 
# sudo apt intall python3-pip
#We'll use pip to create a virtual env, we'll use it on this machine as well like before (in the beginning)
# sudo pip3 install virtualenv  
#Now we install postgres 
# sudo apt install postgresql postgresql-contrib -y
#Before trying to connect it to our local machine, we'll connect from the ubuntu VM  
#CLI for accessing the postgres db is psql
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


