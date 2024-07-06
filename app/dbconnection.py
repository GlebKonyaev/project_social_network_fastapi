import psycopg
from psycopg.rows import dict_row
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.config import settings


def connection():
    while True:
        try:
            conn = psycopg.connect(
                host=f"{settings.database_hostname}",
                dbname=f"{settings.database_name}",
                user=f"{settings.database_username}",
                password=f"{settings.database_password}",
                row_factory=dict_row,
            )
            print("database connection was succesfull ")
            return conn
        except Exception as e:
            print(f"ошибка {e}")
            time.sleep(2)
            break
