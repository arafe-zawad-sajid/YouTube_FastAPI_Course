from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2  #two dots mean going up a dir
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",  #prefix basically appends "/posts" to any route url
    tags=['Posts']  #tags basically improves readability of our swagger ui doc
)  

#--- Get All Posts---#
#Since we're building a social media app we will retrieve all posts from all users, public
#We want the users to be able to filter how many posts they want to view at once 
#To access query params in FastAPI, we just pass it in as another arg in our path operation func 
#We setup a query param "limit" to limit the no. of posts shown at a time
#We setup a query param "skip" to skip some posts (first ones)
#Based on the limit and offset query params, we'll setup pagination,
#so if page 1 returns 10 posts, we want to skip these 20 for page 2  
#We also want to setup a search func based on keywords in title
#To use space in the URL, we use "%20" in between the words
#     
@router.get("/", response_model=List[schemas.PostOut])  #if we use schemas.Post it will give us validation error
def get_posts(db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user),
              limit: int=10,  #def limit is 10 posts
              skip: int=0,
              search: Optional[str]=""):  #an optional search param
    #search the post title to see if the search keyword is anywhere in the title, it doesn't have to match completely
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #LEFT OUTER JOIN
    #by def it's LEFT INNER JOIN, so we need to set it as OUTER
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip)
    # print(results)  #prints the SQL query
    posts = results.all()
    # print(current_user.password)
    return posts  #instead of sending dict we return post 
                  #FastAPI can automatically serialize it and convert it to JSON

#if you want to retrieve only posts belonging to the current_user, private
#
# @router.get("/", response_model=List[schemas.Post])
# def get_posts(db: Session=Depends(get_db), 
#               current_user: models.User=Depends(oauth2.get_current_user)):  #leaving it as int still works
#     posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
#     return posts


#--- Create Posts ---#
#sending status code with the decorator
#we define the reponse model within the decorator
# 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db),
                 current_user: int=Depends(oauth2.get_current_user)):  #this forces the user to log in before creating posts
    # new_post = models.Post(title=post.title, content=post.content,
    #                        published=post.published)
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())  #auto unpack all fields of pydantic model
    db.add(new_post)  #add it to db
    db.commit()  #commit it
    db.refresh(new_post)  #retrieve the new post we created in db
    return new_post  #sends this to the Post request

#--- Get A Post ---#
#Since we're building a social media app we will retrieve posts from any users, public
# 
@router.get("/{id}", response_model=schemas.PostOut)  #APIRouter prefix appends "/posts" with "/id"
def get_post(id: int, db: Session=Depends(get_db), 
             current_user: int=Depends(oauth2.get_current_user)):  #leaving it as int still works 
                                                                   #as python doesn't enforce data types
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post

#if you want to retrieve only posts belonging to the current_user, private
# 
# @router.get("/{id}", response_model=schemas.Post)
# def get_post(id: int, db: Session=Depends(get_db),
#              current_user: models.User=Depends(oauth2.get_current_user)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found")
#     if post.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="Not authorized to perform requested action")
#     return post

#--- Delete A Post ---#
#sending status code with the decorator
#we need to make sure the current user can delete only his own post
# 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # print(type(post))  #<class 'sqlalchemy.orm.query.Query'>
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#--- Update A Post ---#
# 
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,  #validate the data from frontend that is stored in post with our Post schema
                db: Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):  
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()