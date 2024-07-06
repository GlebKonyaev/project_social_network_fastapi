import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

print(os.getenv("DATABASE_HOSTNAME"))  # для проверки
print(os.getenv("DATABASE_PORT"))  # для проверки
print(os.getenv("DATABASE_PASSWORD"))  # для проверки
print(os.getenv("DATABASE_NAME"))  # для проверки
print(os.getenv("DATABASE_USERNAME"))  # для проверки
print(os.getenv("SECRET_KEY"))  # для проверки
print(os.getenv("ALGORITHM"))  # для проверки
print(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))  # для проверки
