from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from .logger_config import setup_logging

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def init_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Логирование
    setup_logging(app)
