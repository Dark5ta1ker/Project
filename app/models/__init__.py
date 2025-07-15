# Импортируем ENUM типы и db из базового файла
from .base import room_type, room_status, booking_status, payment_method, payment_status
from flask_sqlalchemy import SQLAlchemy

# Инициализируем db здесь, чтобы все модели могли импортировать из этого места
db = SQLAlchemy()

# Импортируем все модели
from .guest import Guest
from .room import Room
from .booking import Booking
from .service import Service
from .booking_service import BookingService
from .payment import Payment
from .cleaning_schedule import CleaningSchedule

# Экспортируем все, что может понадобиться в других модулях
__all__ = [
    'db',
    'room_type',
    'room_status',
    'booking_status',
    'payment_method',
    'payment_status',
    'Guest',
    'Room',
    'Booking',
    'Service',
    'BookingService',
    'Payment',
    'CleaningSchedule'
]