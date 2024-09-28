from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import  schemas, models, oauth2

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND0, detail="post does not exists")
    
    vote_quary = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_quary.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already voted on the post")
        new_vote = models.Vote(post_id= vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "succesfully added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")

        vote_quary.delete(synchronize_session=True)
        db.commit()
        return {"message": "succesfully deleted"}