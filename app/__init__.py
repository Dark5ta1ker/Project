from flask import Flask
from .config import Config
from .extensions import db, ma, migrate, init_extensions
from .api import guests_bp, rooms_bp, bookings_bp, services_bp
from dotenv import load_dotenv

def create_app(config_class=Config):
    
    load_dotenv()
    
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init logging
    init_extensions(app)

    # register blueprints
    app.register_blueprint(guests_bp, url_prefix="/api/guests")
    app.register_blueprint(rooms_bp, url_prefix="/api/rooms")
    app.register_blueprint(bookings_bp, url_prefix="/api/bookings")
    app.register_blueprint(services_bp, url_prefix="/api/services")

    return app
