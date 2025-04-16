#run: "uvicorn v4.main:app" and append: "--reload" for auto reload

#--- Response Model ---#
#just like we can define what a request should look like, we can define what a reponse should look like
#the reponse model defines what a post should look like when we send it back to the user, it should strict to a very specific schema
#we used to send back whatever data we received from the post, but sometimes we don't want to send all attributes tot the user
#we define our response with schema 



from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)  #creates db tables

app = FastAPI()  #fastapi instance


#path operation/route
@app.get("/")  #decorator
async def root():  #function
    return {"message": "welcome to my api"}  #sends this to the Get request


#--- Get Posts---#
@app.get("/posts", response_model=List[schemas.Post])  #response with a list of schemas.Post models
def get_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


#--- Create Posts ---#
#sending status code with the decorator
#we define the reponse model within the decorator
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content,
    #                        published=post.published)
    new_post = models.Post(**post.dict())  #auto unpack all fields of pydantic model
    db.add(new_post)  #add it to db
    db.commit()  #commit it
    db.refresh(new_post)  #retrieve the new post we created in db
    return new_post  #sends this to the Post request


#--- Get A Post ---#
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session=Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post  #instead of sending dict we return post 
                 #FastAPI can automatically serialize it and convert it to JSON


#--- Delete A Post ---#
#sending status code with the decorator
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # print(type(post))  #<class 'sqlalchemy.orm.query.Query'>
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#--- Update A Post ---#
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session=Depends(get_db)):  #validate the data from frontend that is stored in post with our Post schema
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


