#--- Environment Variables ---#
# 

from pydantic_settings import BaseSettings
from pydantic import ValidationError

#setting the env vars
#best practice: all caps, pydantic handles it from a case insensitive pov
#
class Settings(BaseSettings):
    # path: int  #pydantic reads the env vars as str and tries to typecase it to int
    #            #if it's not an int it'll give an error
    database_hostname: str 
    database_port: str  #no need to check if it's an int
    database_username: str
    database_password: str
    database_name: str
    secret_key: str 
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = "v9/.env"

settings = Settings()