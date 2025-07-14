from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Создаем экземпляр Flask
app = Flask(__name__)

# Инициализируем SQLAlchemy
db = SQLAlchemy()

# Импортируем маршруты (если они есть)
from app import models  # noqa