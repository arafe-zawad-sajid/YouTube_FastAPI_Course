#--- With ORM (SQLAlchemy) ---#

#run: "uvicorn app.main:app" and append: "--reload"

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)  #creates db tables

app = FastAPI()  #fastapi instance


#pydantic model/schema
#data is validated according to this schema
class Post(BaseModel):
    title: str  #mandatory property
    content: str  #mandatorty property
    published: bool = True  #optional property


#path operation/route
@app.get("/")  #decorator
async def root():  #function
    return {"message": "welcome to my api"}  #sends this to the Get request


#--- Test Route ---#
# @app.get("/test")
# def test_posts(db: Session=Depends(get_db)):
#     # posts = db.query(models.Post)  #a sql querry that hasn't been run yet
#     posts = db.query(models.Post).all()  #all() runs the sql query
#     # print(posts)  #this is a models.Post obj
#     return {'data': posts}


#--- Get Posts---#
@app.get("/posts")
def get_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


#--- Create Posts ---#
#sending status code with the decorator
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session=Depends(get_db)):
    
    return {"data": new_post}  #sends this to the Post request


#--- Get A Post ---#
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id), ))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}


#--- Delete A Post ---#
#sending status code with the decorator
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING * """, 
                   (str(id), ))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#--- Update A Post ---# #fix it#
@app.put("/posts/{id}")
def update_post(id: int, post: Post):  #validate the data from frontend that is stored in post with our Post schema
    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return {"data": updated_post}










#upto upto 4:44:10 - https://youtu.be/0sOvCWFmrtA?si=1oC2iX2LGr8eMOA9&t=17053