#run: "uvicorn v7.main:app" and append: "--reload" for auto reload

#--- Authentication ---#
#2 main ways: session based and JWT token based
#session based: we store sth on our backend server/API to track if a user is logged in
# 
#How JWT works:
#JWT is stateless, there's nothing on our backend/API/db, we store it on frontend
#frontend/client tries to login using path operation "/login" by providing their credentials (email+pass)
#then we verify the credentials and create a JWT token (looks like a random string but contains info embedded in it)
#then we send a response back from the API with the token
#client uses the token to access resources that require auth
#our app requires a user to be logged in to retrieve posts
#the user will send a request to "/posts" endpoint along with the token in the header of the request
#FastAPI first verifies the token and then sends back the requested data as response
#the API doesn't actually track/store anything, instead the client holds on to the token
#and he provides it to us whenever requried (during requests that require auth)
#
#JWT Token deepdive:
#although the token looks encrypted, it is not, it's made of 3 pieces - header, payload, signature  
#header includes metadata of the token
#payload can contain data to be sent with the token, but since it's not encrypted we have to be careful
#we can send the user id and name within the payload, don't jam too much info, it increases the size of the packet
#signature is a combination of header, payload and secret (a special pass only on our API)
#we take those 3 info and pass it in our signing algo (HS256) and it'll return a signature
#this determines the token's validity, we don't want anyone tampering/changing token's data
#there is no encryption, the signature is just there for data integrity (to ensure data was not tampered)
# 
#Purpose of Signature 
#suppose a user logged in by sending his credentials and our API has created the token 
#only the API server has the "secret", nobody should ever have access to it
#we pass the header, payload and secret to a hashing func to create a signature
#then we send out the token to the user which contains header, payload, signature
#suppose a user wants to hack our app, he sees that the token is not encrypted and he can see all the data
#he decided to change a few bits in the token to gain admin priviledges/role (change role to admin), he could do basically anything
#but no he can't, because the signature in the token was generated with the original header and payload (where role was user)
#so if we create a new signature from the tampered data, it would not match the original token's signature, invalid
#so he needs to create a new signature which matches the data he's sending but he doesn't have "secret", so he can't
#now our API verifies the validity of the token by recreating the signature using the API's secret and the token's header and payload
#then the API compares it with the token's signature, token_signature !=  api_signature, it ensures data integrity
#anybody can see and change the data of the token but they can't generate a proper signature since they don't have access to the secret
#this is why the password is so imp
#  
#How to verify the user's credentials
#user hits the "/login" endpoint with email+pass, pass is plain text
#we check the db based on the email provided, the db will send back all the info including the hashed pass
#but we can't get original pass from the hash, hash is one way
#instead we just compare the db's hashed pass with the hashed version of the user provided pass, they should be equal 
#if it's correct, we go ahead and create token and send it back to the user client  

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


