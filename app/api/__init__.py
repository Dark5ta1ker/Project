from flask import Blueprint

# Создаем общий Blueprint "api"
api_bp = Blueprint("api", __name__)

# Импортируем отдельные роуты
from .guests import guests_bp
from .rooms import rooms_bp
from .bookings import bookings_bp
from .services import services_bp

# Регистрируем под-модули в общем api
api_bp.register_blueprint(guests_bp, url_prefix="/guests")
api_bp.register_blueprint(rooms_bp, url_prefix="/rooms")
api_bp.register_blueprint(bookings_bp, url_prefix="/bookings")
api_bp.register_blueprint(services_bp, url_prefix="/services")
