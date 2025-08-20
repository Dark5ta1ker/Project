from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Импорт моделей (чтобы SQLAlchemy их видел)
from .guest import Guest
from .room import Room
from .booking import Booking
from .service import Service
from .booking_service import BookingService
from .payment import Payment