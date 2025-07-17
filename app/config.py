import os
import logging
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Основные настройки
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Настройки БД
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    LOG_LEVEL = 'INFO'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}