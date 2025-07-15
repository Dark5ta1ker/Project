from . import db
from app.models.base import room_status, room_type

class Room(db.Model):
    """
    Модель для хранения информации о номерах.
    Таблица: rooms (схема hotel).
    """
    __tablename__ = 'rooms'
    __table_args__ = {'schema': 'hotel'}
    
    room_id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    room_number = db.Column(db.String(10), nullable=False, unique=True)  # Номер комнаты
    type = db.Column(room_type, nullable=False)  # Тип комнаты (Basic, Advanced, Business, Dorm)
    capacity = db.Column(db.SmallInteger, nullable=False)  # Вместимость (количество человек)
    daily_rate = db.Column(db.Numeric(10, 2), nullable=False)  # Стоимость за сутки
    status = db.Column(room_status, default='available')  # Статус комнаты (например, available)
    description = db.Column(db.Text)  # Описание (необязательно)
    
    # Связь с таблицами bookings и cleaning_schedule
    bookings = db.relationship('Booking', backref='room', lazy=True)
    cleaning_schedule = db.relationship('CleaningSchedule', backref='room', uselist=False, lazy=True)
    
    def to_dict(self):
        """
        Преобразует объект Room в словарь для сериализации в JSON.
        """
        return {
            'room_id': self.room_id,
            'room_number': self.room_number,
            'type': self.type,
            'capacity': self.capacity,
            'daily_rate': float(self.daily_rate) if self.daily_rate else None,
            'status': self.status,
            'description': self.description,
            'available': self.status == 'available'  # Логическое значение для доступности комнаты
        }