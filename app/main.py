from fastapi import FastAPI
from app.dbconnection import connection
import app.models as models
from app.database import engine
from app.routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

models.Base.metadata.create_all(bind=engine)
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
# conn = connection()
# cur = conn.cursor()
app.include_router(post.rout)
app.include_router(user.rout)
app.include_router(auth.rout)
app.include_router(vote.rout)


@app.get("/")
async def main():
    return {"message": "Hello World"}


print(f"database_hostname: {settings.database_hostname}")
print(f"database_port: {settings.database_port}")
print(f"database_password: {settings.database_password}")
print(f"database_name: {settings.database_name}")
print(f"database_username: {settings.database_username}")
print(f"secret_key: {settings.secret_key}")
print(f"algorithm: {settings.algorithm}")
print(f"access_token_expire_minutes: {settings.access_token_expire_minutes}")
