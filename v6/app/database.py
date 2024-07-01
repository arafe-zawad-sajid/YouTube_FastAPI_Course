from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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