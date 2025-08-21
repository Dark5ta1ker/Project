import os

class Config:
    # базовые настройки
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")
    DEBUG = os.environ.get("DEBUG", "False").lower() in ["true", "1", "yes"]

    # настройки базы Postgres
    DB_USER = os.environ.get("POSTGRES_USER", "postgres")
    DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
    DB_HOST = os.environ.get("POSTGRES_HOST", "db")
    DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
    DB_NAME = os.environ.get("POSTGRES_DB", "hotel")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # логирование
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
