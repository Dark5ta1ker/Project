from flask import Flask
from .config import config

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
    
    return app

def register_blueprints(app):
    from .controllers import guests_bp, rooms_bp, bookings_bp
    app.register_blueprint(guests_bp, url_prefix='/api/guests')
    app.register_blueprint(rooms_bp, url_prefix='/api/rooms')
    app.register_blueprint(bookings_bp, url_prefix='/api/bookings')