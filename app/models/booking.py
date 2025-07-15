from . import db
from app.models.base import booking_status
from datetime import datetime

class Booking(db.Model):
    """
    Модель для хранения информации о бронированиях.
    Таблица: bookings (схема hotel).
    """
    __tablename__ = 'bookings'
    __table_args__ = {'schema': 'hotel'}
    
    booking_id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    guest_id = db.Column(db.Integer, db.ForeignKey('hotel.guests.guest_id'), nullable=False)  # Внешний ключ на guests
    room_id = db.Column(db.Integer, db.ForeignKey('hotel.rooms.room_id'), nullable=False)  # Внешний ключ на rooms
    check_in_date = db.Column(db.Date, nullable=False)  # Дата заезда
    check_out_date = db.Column(db.Date, nullable=False)  # Дата выезда
    status = db.Column(booking_status, default='confirmed')  # Статус бронирования
    adults = db.Column(db.SmallInteger, nullable=False, default=1)  # Количество взрослых
    children = db.Column(db.SmallInteger, nullable=False, default=0)  # Количество детей
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)  # Дата создания бронирования
    
    # Связи с таблицами booking_services и payments
    services = db.relationship('BookingService', backref='booking', lazy=True)
    payments = db.relationship('Payment', backref='booking', lazy=True)
    
    def to_dict(self):
        """
        Преобразует объект Booking в словарь для сериализации в JSON.
        """
        return {
            'booking_id': self.booking_id,
            'guest_id': self.guest_id,
            'room_id': self.room_id,
            'check_in_date': self.check_in_date.isoformat(),
            'check_out_date': self.check_out_date.isoformat(),
            'status': self.status,
            'adults': self.adults,
            'children': self.children,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'guest_name': f"{self.guest.first_name} {self.guest.last_name}" if self.guest else None,
            'room_number': self.room.room_number if self.room else None
        }