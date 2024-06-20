from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  #setting passlib def algo

def hash(password: str):
    return pwd_context.hash(password)