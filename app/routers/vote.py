from typing import List, Optional
from fastapi import Depends, HTTPException, Response, status, FastAPI, APIRouter
from app import schemas, database, oauth2
from app.database import get_db, engine
from sqlalchemy.orm import Session
from app import oauth2
from dbconnection import connection
from app.models import PostDB, Votes

# models.Base.metadata.create_all(bind=engine)
rout = APIRouter(prefix="/vote", tags=["Vote"])
# conn = connection()
# cur = conn.cursor()


@rout.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user=Depends(oauth2.get_current_user),
):
    post = db.query(PostDB).filter(PostDB.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {vote.id} does not exist",
        )
    vote_query = db.query(Votes).filter(
        Votes.post_id == vote.post_id, Votes.user_id == current_user.id
    )
    found_query = vote_query.first()
    if vote.dir == 1:
        if found_query:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user with id {current_user.id} already votes on post {vote.post_id}",
            )
        new_post = Votes(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_post)
        db.commit()
        return {"message": "you succesfully create votes"}
    else:
        if not found_query:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="votes does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "you succesfully delete votes"}
