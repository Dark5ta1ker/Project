from .guests import guests_bp
from .rooms import rooms_bp
from .bookings import bookings_bp
from .services import services_bp
from .payments import payments_bp
from .cleaning import cleaning_bp
from .ui import ui_bp

__all__ = [
    'guests_bp',
    'rooms_bp',
    'bookings_bp',
    'services_bp',
    'payments_bp',
    'cleaning_bp',
    'ui_bp'
]