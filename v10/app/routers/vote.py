#--- Voting System ---#
#This will handle all the routing for voting
#We setup a new path called "/vote"  
#user_id will be extracted from the JWT token (like we did in "post.py")
#we don't need to extract that from the body, we don't need to include it in the body
#the body will contain post_id and vote_direction
#vote_dir=1 means like and vote_dir=0 means remove like
#     
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
#since we expect the user to provide some data in the body we need to define a schema for valdiation
# 
def vote(vote: schemas.Vote, db: Session=Depends(database.get_db),
         current_user: int=Depends(oauth2.get_current_user)):
    # checking to see if post exists in the first place  
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.post_id} does not exist")
    # checking to see if vote already exists
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:  #user wants to like a post
        if found_vote:  #but user already liked that post
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        #user will like this post now
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:  #user wants to remove like
        if not found_vote:  #but user has not liked this post
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="vote does not exist")
        #user will delete this like now
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}