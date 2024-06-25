from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")  #tokenUrl is our login endpoint from "auth.py"

#to get a string like this run: openssl rand -hex 32
#bad to harcode "SECRET_KEY" in code, in future we'll turn these in env vars to avoid hardcoding 
#updated using env vars
# 
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes  #after time runs out he can't use the token because it expires

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  #just appends it
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#"get_current_user()" calls this func and expects us to return the token data
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  #stores our payload data
                                                                         #here "algorithms" expects a list
        # print(payload)  #{'user_id': 11, 'exp': 1719003013}
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)  #we validate the actual token data with a schema
    except JWTError:
        raise credentials_exception  #for any kind of error we didn't account for
    return token_data

#we can pass this as a dependency into any path operation   
#it's going to take the token from the request automatically and extract the id for us 
#it's going to verify whether the token is correct
#then it's going to extract the id and automatically fetch the user from db
#and then add it as a param into our path operation func
#anytime we have a specific endpoint that should be protected,
#meaning, the user needs to be logged in to use it,
#we just add this in as an extra dependency into the path operation func
#suppose, users have to be logged in to create a post
#so we just add this as a dependency into the path operation func "create_posts()"
#so any time a user wants to access a resource that requires them to be logged in,
#we're going to expect them to provide an access token
#then we provide this dependency which will call "get_current_user()" 
#and then we pass in the token that comes from the request
#then we run "verify_access_token()" which will verify the access token
#if we return some kind of error that means the token was wrong
#if we return nothing, it means the token is okay
def get_current_user(token: str=Depends(oauth2_scheme), db: Session=Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    #fetch the user from the db so that we can attach the user to any path operation
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

