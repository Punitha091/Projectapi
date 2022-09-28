# from signal import raise_signal
from fastapi import FastAPI,HTTPException,Response,status,APIRouter,Depends
from sqlalchemy.orm import Session
import schema,models,utils
from . import oauth2
from database import engine, get_db

router=APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("")
def create_vote(vote:schema.Vote,db:Session=Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    votes=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    print("post exist")
    print(current_user.id)
    if not votes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" Post doesn't exist with {current_user.id} ")
    vote_query= db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)

    found_vote=vote_query.first()
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user{current_user.id} has already voted on post {vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message":"successfully added vote"}
    elif(vote.dir==0):
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"You did neither like nor dislike with id of {current_user.id}  to the post of {vote.post_id}")




