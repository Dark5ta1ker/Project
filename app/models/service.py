from . import db

class Service(db.Model):
    """
    Модель для хранения информации об услугах.
    Таблица: services (схема hotel).
    """
    __tablename__ = 'services'
    __table_args__ = {'schema': 'hotel'}
    
    service_id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    name = db.Column(db.String(100), nullable=False)  # Название услуги
    description = db.Column(db.Text)  # Описание (необязательно)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Стоимость услуги
    is_active = db.Column(db.Boolean, default=True)  # Флаг активности услуги
    
    # Связь с таблицей booking_services
    bookings = db.relationship('BookingService', backref='service', lazy=True)
    
    def to_dict(self):
        """
        Преобразует объект Service в словарь для сериализации в JSON.
        """
        return {
            'service_id': self.service_id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else None,
            'is_active': self.is_active
        }