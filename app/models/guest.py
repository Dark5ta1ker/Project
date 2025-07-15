from . import db
from datetime import datetime  # Для работы с датами и временем

class Guest(db.Model):
    """
    Модель для хранения информации о гостях.
    Таблица: guests (схема hotel).
    """
    __tablename__ = 'guests'
    __table_args__ = {'schema': 'hotel'}  # Указываем схему базы данных
    
    guest_id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    passport_number = db.Column(db.String(20), nullable=False, unique=True)  # Уникальный номер паспорта
    first_name = db.Column(db.String(50), nullable=False)  # Имя гостя
    last_name = db.Column(db.String(50), nullable=False)  # Фамилия гостя
    phone = db.Column(db.String(20), nullable=False)  # Телефон
    email = db.Column(db.String(100))  # Электронная почта (необязательно)
    address = db.Column(db.Text)  # Адрес (необязательно)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)  # Дата создания записи
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)  # Дата обновления
    
    # Связь с таблицей bookings через обратную ссылку 'guest'
    bookings = db.relationship('Booking', backref='guest', lazy=True)
    
    def to_dict(self):
        """
        Преобразует объект Guest в словарь для сериализации в JSON.
        """
        return {
            'guest_id': self.guest_id,
            'passport_number': self.passport_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'address': self.address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }