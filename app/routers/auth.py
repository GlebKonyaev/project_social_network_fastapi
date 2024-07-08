from fastapi import Depends, HTTPException, Response, status, FastAPI, APIRouter
from sqlalchemy.orm import Session
from app import database, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.models import UserDB


rout = APIRouter(tags=["Authentefication"])


@rout.post("/login")
def user_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = db.query(UserDB).filter(UserDB.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials!",
        )
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials!"
        )
    acces_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": acces_token}
