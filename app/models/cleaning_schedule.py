from . import db

class CleaningSchedule(db.Model):
    """
    Модель для хранения расписания уборки.
    Таблица: cleaning_schedule (схема hotel).
    """
    __tablename__ = 'cleaning_schedule'
    __table_args__ = {'schema': 'hotel'}
    
    id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    needs_cleaning = db.Column(db.Boolean, default=False)  # Флаг необходимости уборки
    next_cleaning_date = db.Column(db.Date)  # Дата следующей уборки
    room_id = db.Column(db.Integer, db.ForeignKey('hotel.rooms.room_id'), unique=True, nullable=False)  # Внешний ключ на rooms
    
    def to_dict(self):
        """
        Преобразует объект CleaningSchedule в словарь для сериализации в JSON.
        """
        return {
            'id': self.id,
            'needs_cleaning': self.needs_cleaning,
            'next_cleaning_date': self.next_cleaning_date.isoformat() if self.next_cleaning_date else None,
            'room_id': self.room_id,
            'room_number': self.room.room_number if self.room else None
        }