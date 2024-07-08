from typing import List, Optional
from fastapi import Depends, HTTPException, Response, status, FastAPI, APIRouter
from app import schemas
from app.database import get_db
from sqlalchemy.orm import Session
from app import oauth2
from sqlalchemy import func
from app.database import get_db
from app.models import PostDB, Votes


# models.Base.metadata.create_all(bind=engine)
rout = APIRouter(prefix="/posts", tags=["Posts"])
# conn = connection()
# cur = conn.cursor()


@rout.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):

    posts = (
        db.query(PostDB, func.count(Votes.post_id).label("votes"))
        .join(Votes, Votes.post_id == PostDB.id, isouter=True)
        .group_by(PostDB.id)
        .filter(PostDB.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    response = []
    for post, votes in posts:
        post_data = post.__dict__.copy()
        post_data["votes"] = votes
        post_data["owner"] = post.owner
        response.append(schemas.PostOut(post=schemas.Post(**post_data), votes=votes))

    return response


# Прокидываем ошибку дальше для обработки FastAPI


@rout.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = PostDB(**post.dict(), owner_id=current_user.id)
    print(current_user.email, current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@rout.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    psot = (
        db.query(PostDB, func.count(Votes.post_id).label("votes"))
        .join(Votes, Votes.post_id == PostDB.id, isouter=True)
        .group_by(PostDB.id)
        .filter(PostDB.id == id)
        .first()
    )
    if psot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} was not found",
        )
    post, votes = psot
    return {"post": post, "votes": votes}
    return psot


@rout.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    deleted_post = db.query(PostDB).filter(PostDB.id == id)
    if deleted_post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} does not found",
        )
    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    deleted_post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@rout.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    updated_post = db.query(PostDB).filter(PostDB.id == id)
    check = updated_post.first()
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} was not found",
        )
    if check.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()
