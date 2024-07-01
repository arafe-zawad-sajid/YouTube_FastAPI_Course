from typing import List
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2  #two dots mean going up a dir


router = APIRouter(
    prefix="/posts",  #prefix basically appends "/posts" to any route url
    tags=['Posts']  #tags basically improves readability of our swagger ui doc
)  

#--- Get Posts---#
@router.get("/", response_model=List[schemas.Post])  #response with a list of schemas.Post models
def get_posts(db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts  #instead of sending dict we return post 
                  #FastAPI can automatically serialize it and convert it to JSON

#--- Create Posts ---#
#sending status code with the decorator
#we define the reponse model within the decorator
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db),
                 current_user: int=Depends(oauth2.get_current_user)):  #this forces the user to log in before creating posts
    # new_post = models.Post(title=post.title, content=post.content,
    #                        published=post.published)
    # print(current_user.email)
    new_post = models.Post(**post.dict())  #auto unpack all fields of pydantic model
    db.add(new_post)  #add it to db
    db.commit()  #commit it
    db.refresh(new_post)  #retrieve the new post we created in db
    return new_post  #sends this to the Post request

#--- Get A Post ---#
@router.get("/{id}", response_model=schemas.Post)  #APIRouter prefix appends "/posts" with "/id"
def get_post(id: int, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

#--- Delete A Post ---#
#sending status code with the decorator
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # print(type(post))  #<class 'sqlalchemy.orm.query.Query'>
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#--- Update A Post ---#
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,  #validate the data from frontend that is stored in post with our Post schema
                db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):  
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()