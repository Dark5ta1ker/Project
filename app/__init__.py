from flask import Flask
from app.models import db

def create_app():
    """Фабрика приложений"""
    # Создаем экземпляр Flask
    app = Flask(__name__)
    
    # Конфигурация приложения
    app.config.from_object('app.config.Config')
    
    # Инициализируем расширения
    db.init_app(app)
    
    # Регистрируем обработчики ошибок
    from .error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Импортируем и регистрируем blueprints
    # register_blueprints(app)
    
    return app

# def register_blueprints(app):
#     """Регистрация всех blueprint'ов приложения"""
#     # Пример для модуля гостей
#     from .controllers.guests_controller import guests_bp
#     app.register_blueprint(guests_bp, url_prefix='/api/guests')
    
#     # Другие модули
#     from .controllers.rooms_controller import rooms_bp
#     app.register_blueprint(rooms_bp, url_prefix='/api/rooms')
    
    # Добавьте остальные blueprint'ы по аналогии
    # from .controllers.bookings_controller import bookings_bp
    # app.register_blueprint(bookings_bp, url_prefix='/api/bookings')