#run: "uvicorn v14.app.main:app" and append: "--reload" for auto reload
 
#--- Application Deployment (NGINX) ---#
#Currently when we send a request to our server, the specific ip and port we configured our app to listen on 
#we send that request directly to the app (i.e. gunicorn), this is okay
#But professionally we have an intermediary web server, which will receive the request and act as a proxy
#and proxy that request to our specific app (i.e. gunicorn), one of the most common is NGINX, HAProxy, Traffic
#NGINX is optimzed for SSL termination, it's a high performance server  
#When we send a HTTP request to our NGINX server, it'll process it and forward it as plain HTTP packet to our app 
#It's not optimzed for HTTPS but it could be configured 
#On our app, when we start adding responsibilities like performing SSL offload, we'll see a degradation in performance
#NGINX is optimzed for this so it's best to give this responsibility to NGINX instead of our app
#We're gonna configure NGINX, it'll act as a gateway into our system so any request we send
#whether it's HTTP/HTTPS , we're gonna send it to NGINX 
#If we send HTTPS, NGINX will take it and forward it as HTTP packet to our app
# sudo apt install nginx -y
# systemctl start nginx
#Now if we go to our ip, it'll show default NGINX welcome page, we'll change this
# cd /etc/nginx/sites-available/
# ls
# cat default
#Here we can see that it listens on port 80 by default and the welcome page file is in "root /var/www/html;"
#server_name is the domain name it'll handle request for, ignore other stuff for now
#The only thing we want to change here is the location block, see the example file "nginx" 
#What the location block is saying is any request that matches the root path and beyond is proxied to localhost:8000
#we specify the ip and port we want to proxy traffic for, we'll forward it to gunicorn on port 8000 
#The other lines are for optimization, we don't need it now    
#So we copy paste what's in the location block to the "default" file
# systemctl restart nginx
#Now if we visit our ip we see our api. We see it's HTTP, let's set it to HTTPS. We'll need to purchase a domain name.
#We can purchase from namecheap/go daddy/amazon, ".xyz" is the cheapest domain
#Now we have to setup a couple of rules. We need to point our domain name to digital ocean. We can use their guide.
# https://docs.digitalocean.com/products/networking/dns/getting-started/dns-registrars/
#For Namecheap, under the "name server" section we have to set "custom DNS" and point to the DNS servers of Digital Ocean  
#On digital ocean, goto "manage DNS" and add the domain. 
#Then create "A Record" (root of our domain) where hostname is '@' and direct it to the droplet.
#So if we visit our domain, it'll take us to our digital ocean server. We need to wait upto an hour for the DNS to propagate.
#We also create a "CNAME Record" with hostname as "www", alias of "@". The "CNAME Record" points to "A Record" 
#We can visit the domain in both ways (through the domain and the sub-domain) 
#Now we setup the SSL to handle secure HTTPS traffic.
#"certbot" is a website for "lets encrypt" which is a free SSL service. We select "get certbot instructions" and follow it.
# https://certbot.eff.org/
#It'll auto reconfigure NGINX for us.     
#First we see if "snapd" is installed, let's check it
# snap --version
#Now we install certbot
# sudo snap install --classic certbot
#Now we want certbot to auto configure NGINX for us
# sudo certbot --nginx  
#when it asks for the domain name we put both "A Record" (domain) and "CNAME Record" (sub-domain)
#It'll edit our "default" config file in /etc/nginx/sites-enabled/default 
#The main change is the server block for SSL configuration, we're gonna listen on port 443 (default https port),
#added the two certificates that were generated, added a few other configs   
#It also added another server block to redirect http request to https, we'll never be able to use http from now on 
#Now when we visit our domain/sub-domain we'll see both are https, now we have https setup on our nginx server 
#We want nginx to auto start on reboot, this is the default config though 
# systemctl status nginx
#If it's disabled we just enable it
# systemctl enable nginx
#Now we setup a firewall on our machine for basic security, we make sure we only open ports that we'll be using
#Right now we can access any port, but we don't want people to connect to diff services on our machine 
# sudo ufw status
# sudo ufw allow http
# sudo ufw allow https
#Since it's a public server, we allow for all http and https traffic
# sudo ufw allow ssh
#We allow this to be able to ssh to the server from local machine 
# sudo ufw allow 5432
#We don't need to open up our database port since our FastAPI app is running on the server, 
#if we didn't want anyone from outside to access our database we shouldn't allow it, this is better
#but if we want to connect using pgAdmin from local machine then we have to allow it
# sudo ufw enable
# exit
# sudo ufw status
#If you want to delete a rule 
# sudo ufw delete allow http
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


