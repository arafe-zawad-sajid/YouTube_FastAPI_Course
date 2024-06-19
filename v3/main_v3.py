#--- With ORM (SQLAlchemy) ---#

#run: "uvicorn app.main:app" and append: "--reload" for auto reload

from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)  #creates db tables

app = FastAPI()  #fastapi instance


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
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()  #retrieve multiple posts

    posts = db.query(models.Post).all()
    return {"data": posts}


#--- Create Posts ---#
#sending status code with the decorator
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()  #save finalized staged changes

    # new_post = models.Post(  #create a new post
    #     title=post.title, content=post.content, published=post.published)
    
    new_post = models.Post(**post.dict())  #auto unpack all fields of pydantic model
    db.add(new_post)  #add it to db
    db.commit()  #commit it
    db.refresh(new_post)  #retrieve the new post we created in db
    return {"data": new_post}  #sends this to the Post request


#--- Get A Post ---#
@app.get("/posts/{id}")
def get_post(id: int, db: Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id), ))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
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


#--- Update A Post ---# #fix it#
@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session=Depends(get_db)):  #validate the data from frontend that is stored in post with our Post schema
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


#schema/pydantic model vs. orm/sql alchemy model
#schemas.Post class extends BaseModel which is imported from pydantic lib, this is our schema
#it's being referenced in our path operations, it defines the shape of our requests and response
#validates the schema, it tells the user what we exactly need for each path/route
#it ensures that everything matches up with what we expect
#models.Post class is our sql alchemy model, it defines what our db table looks like
#it is used to perform queries within our db



#upto upto 5:39:00 - https://youtu.be/0sOvCWFmrtA?si=Pg2BZ-GBKjk0e1a2&t=20350