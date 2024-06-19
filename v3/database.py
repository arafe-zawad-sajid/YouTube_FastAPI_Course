from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://<user>:<pass>@<server ip or hostname>/<db name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi'  #connection string

#the engine is responsible for connecting sql alchemy to postgresql 
engine = create_engine(SQLALCHEMY_DATABASE_URL)  #only for sqlite we have to pass connect_args as 2nd param

#to talk to the sql db we make use of a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  #all models that we'll define to create our tables will extend this Base class


#dependency: the func connects/gets a session to db
#we can keep calling this func every time we get a request to any of our API endpoints
def get_db():
    db = SessionLocal()  #session obj resposible for talking with db
    try:
        yield db
    finally:
        db.close()