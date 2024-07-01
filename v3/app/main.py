#run: "uvicorn v3.main:app" and append: "--reload" for auto reload

#--- With ORM (SQLAlchemy) ---#
#one way to interract with the db is to use the def postgresql driver (psycopg2) 
#to talk to a postgresql db using sql queries
#another way to work with db is to use orm, it's a layer abstraction between our db and fastapi app
#instead of talking directly to a db we talk to the orm which will in turn talk to the db
#no more sql, we use python code that ultimately translates to sql themselves
#when using orm we don't rely on regular sql queries, instead we use some basic python method
#traditionally, our fastapi server talks to our db by sending sql using def postgresql driver (psycopg2)
#for orm, fastapi uses regular python to send commands to orm 
#which converts it to regular sql using the same db driver (psycopg2) to talk to the db
#databases only talk sql
#sql alchemy is the most popular python orm, it's a standalone lib
#sql alchemy doesn't actually know how to talk to a db, it uses the underlying driver psycopg2
#
#schema/pydantic model vs. orm/sql alchemy model
#Post class extends BaseModel which is imported from pydantic lib, this is our schema
#it's being referenced in our path operations, it defines the shape of our requests and response
#we take the request and pass it to the pydantic model which will perform validation
#to make sure we have all the fields that we need and are of the proper type
#validates all the data fields provided in the body according to the schema
#it tells the user what we exactly need for each specific path/route
#similarly we define exactly what the response should look like
#we define a model to dictate FastAPI exactly the data fields that we should be sending back
#pydantic/schema model ensures that the request and response are shaped in a specific way
#technically we don't need pydantic models but it allows us to be strict when sending/receiving data
#it ensures that everything matches up with what we expect
#schema and orm models are diff
#models.Post class is our sql alchemy model, it defines what our db table looks like
#it is used to perform queries within our db



# from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)  #creates db tables based on models.Base schema

app = FastAPI()  #fastapi instance


#--- Connecting to Database ---#
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', 
#                                 user='postgres', password='admin', cursor_factory=RealDictCursor)
# 
#         cursor = conn.cursor()
#         print('DB conn was successful')
#         break
#     except Exception as error:
#         print('DB conn failed')
#         print('Error:', error)
#         time.sleep(2)


#path operation/route
@app.get("/")  #decorator
async def root():  #function
    return {"message": "welcome to my api"}  #sends this to the Get request


#--- Test Route ---#
# @app.get("/test")
# def test_posts(db: Session=Depends(get_db)):  #database.get_db() is a dependency, makes testing easier
#     # posts = db.query(models.Post)  #to make a query we access the db obj
#                                      #models.Post allows us to access that model,
#                                      #to make a query to our "posts" table
#                                      #these models represent tables
#                                      #posts is a query obj that contains a sql that hasn't been run yet
#     posts = db.query(models.Post).all()  #all() runs the sql query and grabs all entry within "posts" table
#     # print(posts)  #this is a models.Post obj
#     return {'data': posts}


#--- Get Posts---#
@app.get("/posts")
def get_posts(db: Session=Depends(get_db)):  #this input arg creates a session to our db so that we can perform some operations
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()  #retrieve multiple posts

    posts = db.query(models.Post).all()
    return {"data": posts}


#--- Create Posts ---#
#sending status code with the decorator
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, db: Session=Depends(get_db)):  #Post pydantic model defines the shape of our requests
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()  #save finalized staged changes

    # new_post = models.Post(title=post.title, content=post.content,
    #                        published=post.published)  #create a new post
    #post.dict() gives us a dict which we need to convert to the above format
    new_post = models.Post(**post.dict())  #auto unpack all fields of pydantic model 
                                           #if we add an extra field to our model it will still work
    db.add(new_post)  #add it to db
    db.commit()  #commit it
    db.refresh(new_post)  #retrieve the new post we created in db
    return {"data": new_post}  #sends this to the Post request


#--- Get A Post ---#
@app.get("/posts/{id}")
def get_post(id: int, db: Session=Depends(get_db)):  #db dependency in our path operation func
    # cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id), ))
    # post = cursor.fetchone()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)  #filter() is like sql WHERE
    # print(post_query)  #post_query contains sql
    post = post_query.first()  #if we used all() instead it would keep on looking unnecessarily
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}


#--- Delete A Post ---#
#sending status code with the decorator
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING * """, 
    #                (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # print(type(post))  #<class 'sqlalchemy.orm.query.Query'>
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#--- Update A Post ---#
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.Post, db: Session=Depends(get_db)):  #validate the data from frontend that is stored in post with our Post schema
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)  #query
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)  #update
    db.commit()  #commit
    return {"data": post_query.first()}  #get the first one



