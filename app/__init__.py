from flask import Flask
from app.models import db
from app.config import Config
from app.utils.logger_config import setup_logger
from app.utils.error_handlers import register_error_handlers
from app.controllers import (
    guests_bp, rooms_bp, bookings_bp,
    services_bp, payments_bp, cleaning_bp,
    ui_bp
)

logger = setup_logger()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Инициализация расширений
    db.init_app(app)
    
    # Регистрация обработчиков ошибок
    register_error_handlers(app)
    
    # Регистрация Blueprints
    app.register_blueprint(guests_bp, url_prefix='/api/guests')
    app.register_blueprint(rooms_bp, url_prefix='/api/rooms')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    app.register_blueprint(services_bp, url_prefix='/api/services')
    app.register_blueprint(payments_bp, url_prefix='/api/payments')
    app.register_blueprint(cleaning_bp, url_prefix='/api/cleaning-schedule')
    app.register_blueprint(ui_bp)
    
    return app