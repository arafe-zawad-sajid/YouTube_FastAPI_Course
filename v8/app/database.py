import psycopg2
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#--- Connecting to Database ---#
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', 
#                                 user='postgres', password='admin', cursor_factory=RealDictCursor)
        
#         cursor = conn.cursor()
#         print('DB conn was successful')
#         break
#     except Exception as error:
#         print('DB conn failed')
#         print('Error:', error)
#         time.sleep(2)


#We shouldn't hardcode the database url, anyone can see it
#In a production env, we need a way for our code to auto update and point to the actual production db 
#Any kind of confidential info or anything that needs to be updated based off of the env that it's in
#We will make use of Environment Variables
# 
# SQLALCHEMY_DATABASE_URL = 'postgresql://<user>:<pass>@<server ip or hostname>/<db name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi'
engine = create_engine(SQLALCHEMY_DATABASE_URL)  #only for sqlite we have to pass connect_args
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#the function connects/get a session to db
def get_db():
    db = SessionLocal()  #session obj resposible for talking with db
    try:
        yield db
    finally:
        db.close()