from . import db
from datetime import datetime

class BookingService(db.Model):
    """
    Модель для хранения информации об услугах, связанных с бронированием.
    Таблица: booking_services (схема hotel).
    """
    __tablename__ = 'booking_services'
    __table_args__ = {'schema': 'hotel'}
    
    booking_service_id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    booking_id = db.Column(db.Integer, db.ForeignKey('hotel.bookings.booking_id'), nullable=False)  # Внешний ключ на bookings
    service_id = db.Column(db.Integer, db.ForeignKey('hotel.services.service_id'), nullable=False)  # Внешний ключ на services
    quantity = db.Column(db.SmallInteger, nullable=False, default=1)  # Количество услуг
    service_date = db.Column(db.Date, default=datetime.utcnow().date())  # Дата оказания услуги
    notes = db.Column(db.Text)  # Примечания (необязательно)
    
    def to_dict(self):
        """
        Преобразует объект BookingService в словарь для сериализации в JSON.
        """
        return {
            'booking_service_id': self.booking_service_id,
            'booking_id': self.booking_id,
            'service_id': self.service_id,
            'quantity': self.quantity,
            'service_date': self.service_date.isoformat() if self.service_date else None,
            'notes': self.notes,
            'service_name': self.service.name if self.service else None,
            'total_price': float(self.service.price * self.quantity) if self.service and self.service.price else None
        }