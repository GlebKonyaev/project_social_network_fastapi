# Используем базовый образ Python
FROM python:3.12.3-slim

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование исходного кода
COPY . /app
WORKDIR /app

# Запуск приложения с помощью uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
