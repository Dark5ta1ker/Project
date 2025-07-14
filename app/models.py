from app import db  # Импортируем объект базы данных из приложения
from datetime import datetime  # Для работы с датами и временем
from sqlalchemy.dialects.postgresql import ENUM  # Для создания пользовательских типов ENUM в PostgreSQL

# Создаем пользовательские типы ENUM для PostgreSQL
# Эти типы используются для ограничения значений полей в таблицах базы данных
room_type = ENUM('Basic', 'Advanced', 'Business', 'Dorm', name='room_type', create_type=True)
room_status = ENUM('available', 'occupied', 'maintenance', 'cleaning', name='room_status', create_type=True)
booking_status = ENUM('confirmed', 'checked_in', 'checked_out', 'cancelled', name='booking_status', create_type=True)
payment_method = ENUM('cash', 'credit_card', 'bank_transfer', 'online', name='payment_method', create_type=True)
payment_status = ENUM('pending', 'completed', 'failed', 'refunded', name='payment_status', create_type=True)

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

class Payment(db.Model):
    """
    Модель для хранения информации о платежах.
    Таблица: payments (схема hotel).
    """
    __tablename__ = 'payments'
    __table_args__ = {'schema': 'hotel'}
    
    payment_id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    booking_id = db.Column(db.Integer, db.ForeignKey('hotel.bookings.booking_id'), nullable=False)  # Внешний ключ на bookings
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # Сумма платежа
    method = db.Column(payment_method, nullable=False)  # Метод оплаты
    status = db.Column(payment_status, default='pending')  # Статус платежа
    transaction_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)  # Дата транзакции
    notes = db.Column(db.Text)  # Примечания (необязательно)
    
    def to_dict(self):
        """
        Преобразует объект Payment в словарь для сериализации в JSON.
        """
        return {
            'payment_id': self.payment_id,
            'booking_id': self.booking_id,
            'amount': float(self.amount) if self.amount else None,
            'method': self.method,
            'status': self.status,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'notes': self.notes
        }

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