from fastapi import FastAPI
from app.dbconnection import connection
import models
from database import engine
from routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
conn = connection()
cur = conn.cursor()
app.include_router(post.rout)
app.include_router(user.rout)
app.include_router(auth.rout)
app.include_router(vote.rout)


@app.get("/")
async def main():
    return {"message": "Hello World"}
