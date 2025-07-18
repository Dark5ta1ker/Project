from flask import Flask
from .config import config
from .controllers import guests_bp, rooms_bp, bookings_bp, cleaning_bp, payments_bp, services_bp, ui_bp

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Загрузка конфигурации
    cfg = config[config_name]
    app.config.from_object(cfg)
    
    # Инициализация БД
    from .models import db
    db.init_app(app)
    
    # Регистрация обработчиков ошибок
    from .utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Регистрация маршрутов
    register_blueprints(app)
    
    if config_name not in config:
        raise ValueError(f"Config '{config_name}' not found")
    
    return app

def register_blueprints(app):
    app.register_blueprint(guests_bp, url_prefix='/api/guests')
    app.register_blueprint(rooms_bp, url_prefix='/api/rooms')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
    app.register_blueprint(cleaning_bp, url_prefix='/api/cleanings')
    app.register_blueprint(payments_bp, url_prefix='/api/payments')
    app.register_blueprint(services_bp, url_prefix='/api/services')
    app.register_blueprint(ui_bp, url_prefix='/ui')

