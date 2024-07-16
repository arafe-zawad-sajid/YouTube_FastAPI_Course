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
#to ssh my ubuntu server vm we do 
# ssh azs@ip-address
# sudo -i
#this will log us in to root
#Select yes and put the password for the VM
# ls
#It'll show the content of our current dir, currently we've only one
#First thing to do is to updated all of the installed packages  
# sudo apt update && sudo apt upgrade -y
#You can "keep the local version" or "install the package maintainer's version", we select maintainer's version
# python3 --version
#This will work, but if we type only python it won't work
#We install pip if we don't have it installed 
# sudo apt install python3-pip -y
#We'll use pip to create a virtual env, we'll use it on this machine as well like before (in the beginning)
# sudo pip3 install virtualenv  
#Now we install postgres 
# sudo apt install postgresql postgresql-contrib -y
#Before trying to connect it to our local machine, we'll connect from the ubuntu VM  
#CLI for accessing the postgres db is psql
# psql --version
#Like before we log in to postgres using the def user "postgres" 
# psql -U postgres
#It'll give "peer authentication error", it's not a usual log in failure 
#On ubuntu, postgres has a special way of authenticating users by def 
#When the ubuntu VM tries to connect to the db itself, it's called local auth
#Whereas, when we connect from our Windows machine to the postgres db on this ubuntu VM, that is peer auth
#Since we're on the same machine that we're trying to connect to our db, postgres considers this as local auth
#Peer auth is the def config for postgres, it takes the user that's logged in to the ubuntu machine
#and tries to log in as that user, in this case psql tries to log in as root user 
#It'll only allow a ubuntu user called "postgres" to be able to log in as the user called "postgres" on the postgres db in psql   
#It actually obtains the username from the linux kernel, so whoever you're logged in as is the only person you can log in as    
#Because this is the def config, postgres actually created a user on our Ubuntu VM called "postgres"
#We run this cmd to list out all the users 
# sudo cat /etc/passwd 
#We can see that a user called postgres was created on this machine, we change our user
# su - postgres
#On the left we see we're logged in as user "postgres" 
# psql -U postgres
#We've logged into the db, now we want to get rid of that peer auth
#We'll set up a password for the "postgres" user
# \password postgres
#We exit out of the postgres console/terminal
# \q
#We're still logged in as the "postgres" user, we want to go back to the root user
# exit 
#To modify the configs for postgres, we want to move to a diff dir 
# cd /etc/postgresql/12/main
# ls
#We have to edit the files "postgresql.conf" and "pg_hba.conf"
# sudo vi postgresql.conf
#In the "Connections And Authentication" section we see that listen_address = 'localhost'
#On the ubuntu server vm we set it to "*", meaning all 
#That means, only if we're logged into this ubuntu VM we can connect to this postgres db 
#It'll not allow us to use pgAdmin from our Windows machine and connect to it remotely
#To be able to connect to it remotely we've to change these configs
# listen_addresses = *
#It'll allow me to connect from any ip address but best practice is to restrict it to some for security
# sudo vi pg_hba.conf 
#Now we change the configs under both local, edit "peer" > "md5" for the two local method settings
#Now we change the configs under both host, edit ip adress > "0.0.0.0/0" for ipv4 and "::/0" for ipv6
#We have disabled peer auth and allowed any host ip to access the Ubuntu VM  
#When we change any config file we've to restart the app 
# systemctl restart postgresql
# psql -U postgres
#Enter the password and login to postgres db
#Now we try to connect to it using pgAdmin on our local Windows machine 
#Create server, go to general and set name = fastapi-prod 
#Instead I named it server-laptop 
#go to connection and set host name = ip address of our machine and provide password
#Instead I provide ip address of ubuntu server vm 
#We can see the def postgres db that is always installed
#Generally on Ubuntu we shouldn't be logged in as root user, security risks  
#So we create another user with root priviledges, that's better
#When we install our API or python app, we're going to use this user for starting it
#We don't want the root user to start the app because that would mean 
#we're giving the app root access which is very risky
# adduser azs
#We set the password
# su - azs 
#Or we can exit out of root user and use ssh to directly log in as azs
# ssh azs@ubuntu-vm-ip-address
#Enter the password and log in  
#Any time we create a user we have to give sudo access in order to perform root priviledged operations
# usermod -aG sudo azs  
#exit and connect back as user azs 
# sudo apt upgrade
#Give password 
# pwd
#It gives us the dir we're in, default home is "/home/azs" 
# cd ~
#It takes us to home dir 
#Now we create a folder for our app on our home dir
# mkdir app
# cd app
#now we create a python venv like we did in the beginning of the tutorial 
# virtualenv .venv
# ls -la
#Now we activate the venv
# source .venv/bin/activate  
#On the left side we see the venv activated
# deactivate
#This will deactivate the venv
#Within our app dir we create the folder called "src" 
# mkdir src
# cd src
#Now we copy all our code into the VM. Since we have our code on github, we just copy the repo link from there 
# git clone github-clone-link .
#Here, github-clone-link = github.repo-link.git 
#The dot "." in the end means current dir. This will install our repo in our current dir (/app/src) 
#Activate venv again and move into "src" dir. We don't have any packages installed.      
# cat requirements.txt
# pip install -r requirements.txt
#We're going to get an error saying "libpq" is missing. We need to deactivate the venv and install the apt 
# deactivate
# sudo apt install libpq-dev
#Now we move into the "app" dir and activate our venv 
# cd .. 
# source .venv/bin/activate
#Now we try pip install again from the "app/src" folder 
# cd src
# pip install -r requirements.txt
#Now we try to start our app 
# uvicorn app.main:app
#We get 8 validation errors, we need to setup our env vars on our linux VM
#We can manually set them one by one
# export ENV_VAR_NAME = VALUE
#To see all our def and user created env vars
# printenv
#To delete an env var 
# unset ENV_VAR_NAME
#From our home dir we create an empty file
# cd ~
# touch .env
#Lets check if it was created 
# ls -la
#Lets open the file and edit it 
# vi .env
#Here we provide the list of env vars, but before each env var we must type in "export"
# export ENV_VAR_NAME = VALUE 
#We save and set all the env vars from this file 
# wq 
# source .env
#This will set all of those env vars
# printenv
# cat .env
#We can see that the format is "export ENV_VAR_NAME=VALUE" 
#We try to match the env var file in the ubuntu VM with our local windows machine, just key value pairs 
#Before this modification we need to unset the env vars and printenv to check if they got removed
#We also open up the ".env" file and delete everything, and copy paste the env vars from our ".env" file on windows
# vi .env
# set -o allexport; source /home/azs/.env; set +o allexport 
# printenv
#It worked, but if we reboot we loose our env vars
# sudo reboot
#After the reboot we log in using the ssh command like before and printenv shows our env vars are gone
#To make it persist we edit the ".profile" file on home and save the command that we used to set our env vars   
# cd ~
# ls -la
# vi .profile
#Go to the bottom of the file and paste the following command
# set -o allexport; source /home/azs/.env; set +o allexport
# wq
#If we log out and log in or if we reboot, the env vars will be loaded each time, it'll persist 
#There are other methods to tackle this but this is the simplest 
#Our ".env" file is stored in the home dir and not the app dir, we don't want it to accidentally get uploaded to git 
#Now from windows, we use pgAdmin to create the db, it has no tables
#We also need to make sure ".env" file is updated according to our production env and not our previous development environment 
#In our db we have no tables, we use alembic to setup our tables per our models in our prod env
#We should never create revisions in our prod env, we only create it in our dev env and check it into git 
#We go to "src" dir and do alembic upgrade to setup our db per our latest revision
# cd src
# alembic upgrade head
#It created all of the individual revisions one at a time so that we can roll back like before in our dev env
#Now we activate our venv and move into "app/src/<latest-version>" dir and run the uvicorn command
# uvicorn app.main:app
#We can find the ip-address:port-num that the uvicorn server is running on, so we try to connect to it from our browser 
#But it didn't work, we needed to make sure that it can listen on any ip-address 
#Setting it to "127.0.0.1:8000" means only the ubuntu VM can access it, we need to pass in one more flag 
# uvicorn --host 0.0.0.0 app.main:app
#Now we can go to chrome on our windows and access http://server_vm_ip:port_num
#We don't need to provide a diff port because when we're gonna deploy it's always gonna use port 80 (HTTP) or 443 (HTTPS)   
#Now we can access it on our windows. But if it crashes/reboots, it doesn't restart automatically. 
#We're gonna use a process manager called Gunicorn 20.1.10. From the venv we install it.
# pip install gunicorn
# gunicorn 
#If we get any errors we would need two other packages httptools 0.3.0, uvloop 0.16.0
# pip install httptools
# pip install uvtools 
#it's not uvtools, it's uvloop, later on it was fixed 
#We can have a num of workers and distribute the load balance between them 
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
#We set the ip-address "0.0.0.0" like before and specify a port then we want to listen on
# gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
#We get an error uvloop missing, we just need to install the library 
# pip install uvloop
# pip freeze 
#We should update our "requirements.txt" file and update it on git 
#so when we deploy to other ubuntu machines it'll have all these extra packages
#After it starts up we can see the 4 process id (pid) 
# ps -aef | grep -i gunicorn
#We can see the diff processes that we started, 1 parent and 4 child processes 
#If we refresh chrome on windows we can see that we can access it normally
#Currently it's running on our specific terminal, we want it to run in the background and automatically startup on boot
#So we are going to create our own service that will startup our fastapi app automatically
# cd /etc/systemd/system
# ls
#We can see all of the services installed on our machine, we'll create a new one 
#On the source github repo (sanjeev's) we can see a file "gunicorn.service", we make some edits
#Under [Unit] we just give a description of what it's gonna do
#Line 3 tells our ubuntu vm when to actually start this service
#This basically says that we need our network service running before we can start our API
#Then under [Service] we have to specify what user and group is going to run this service,
#It needs to be associated with a user, these two should be the same (azs)
#The working dir is the dir where our service will be launched in
#this should point to the dir our app is running in, home/azs/app/src/v13 (diff from Sanjeev's) 
#Since we want the service to run the gunicorn cmd, we need it to run in a venv
#so we set the venv through this script, we point it to the "home/azs/app/.venv/bin" folder  
#Now we provide the path where gunicorn resides in (.venv/bin/gunicorn) and the cmd we want to run 
# cd /etc/systemd/system   
#Under this dir we create the "api.servcie" service 
# sudo vi api.service
#Now we just copy paste everything from that "gunicorn.service" file
#Now we start our "api.service" 
# systemctl start api    
#We see that it's not running, that's because it doesn't know where the .env file is
#so we add another line to set the "EnvironmentFile" and then do a daemon reload and restart api
# systemctl daemon-reload 
# systemctl restart api
#We can also setup a config file for our new service but this is easier
#Now we want to setup this service to automatically startup on reboot
# sudo systemctl enable api 
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


