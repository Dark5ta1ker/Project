# Базовый образ с Python
FROM python:3.9-slim

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY app/requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY app/ .

# Порт, на котором будет работать Flask
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "main.py"]