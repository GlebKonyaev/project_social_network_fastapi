from pydantic_settings import BaseSettings
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
load_dotenv()


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()
print(f"database_hostname: {settings.database_hostname}")
print(f"database_port: {settings.database_port}")
print(f"database_password: {settings.database_password}")
print(f"database_name: {settings.database_name}")
print(f"database_username: {settings.database_username}")
print(f"secret_key: {settings.secret_key}")
print(f"algorithm: {settings.algorithm}")
print(f"access_token_expire_minutes: {settings.access_token_expire_minutes}")
