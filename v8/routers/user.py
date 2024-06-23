from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils


router = APIRouter(
    prefix="/users", 
    tags=['Users']
    )

#--- Create User ---#
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    #hash password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#--- Get A User ---#
#we want to setup a route to our path operation that allows us to fetch and retrieve user info based on their id
#it can be part of the auth process
#if we setup JWT tokens to get sent as cookies then the frontend may not know if the user is logged in or not
#also for retrieving a user's profile info
@router.get("/{id}", response_model=schemas.UserOut)  #response_model in the decorator
def get_user(id: int, db: Session=Depends(get_db)):  #db in the function
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    return user