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
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                     models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="vote does not exist")
    vote_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "successfully deleted vote"}