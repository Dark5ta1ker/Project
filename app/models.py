from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import ENUM

# Создаем пользовательские типы ENUM для PostgreSQL
room_type = ENUM('Basic', 'Advanced', 'Buisiness', 'Dorm', name='room_type', create_type=True)
room_status = ENUM('available', 'occupied', 'maintenance', 'cleaning', name='room_status', create_type=True)
booking_status = ENUM('confirmed', 'checked_in', 'checked_out', 'cancelled', name='booking_status', create_type=True)
payment_method = ENUM('cash', 'credit_card', 'debit_card', 'bank_transfer', name='payment_method', create_type=True)
payment_status = ENUM('pending', 'completed', 'failed', 'refunded', name='payment_status', create_type=True)

class Guest(db.Model):
    __tablename__ = 'guests'
    __table_args__ = {'schema': 'hotel'}
    
    guest_id = db.Column(db.Integer, primary_key=True)
    passport_number = db.Column(db.String(20), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    bookings = db.relationship('Booking', backref='guest', lazy=True)
    
    def to_dict(self):
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
    __tablename__ = 'rooms'
    __table_args__ = {'schema': 'hotel'}
    
    room_id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), nullable=False, unique=True)
    type = db.Column(room_type, nullable=False)
    capacity = db.Column(db.SmallInteger, nullable=False)
    daily_rate = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(room_status, default='available')
    description = db.Column(db.Text)
    
    bookings = db.relationship('Booking', backref='room', lazy=True)
    cleaning_schedule = db.relationship('CleaningSchedule', backref='room', uselist=False, lazy=True)
    
    def to_dict(self):
        return {
            'room_id': self.room_id,
            'room_number': self.room_number,
            'type': self.type,
            'capacity': self.capacity,
            'daily_rate': float(self.daily_rate) if self.daily_rate else None,
            'status': self.status,
            'description': self.description,
            'available': self.status == 'available'
        }

class Booking(db.Model):
    __tablename__ = 'bookings'
    __table_args__ = {'schema': 'hotel'}
    
    booking_id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('hotel.guests.guest_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('hotel.rooms.room_id'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    status = db.Column(booking_status, default='confirmed')
    adults = db.Column(db.SmallInteger, nullable=False, default=1)
    children = db.Column(db.SmallInteger, nullable=False, default=0)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    
    services = db.relationship('BookingService', backref='booking', lazy=True)
    payments = db.relationship('Payment', backref='booking', lazy=True)
    
    def to_dict(self):
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
    __tablename__ = 'services'
    __table_args__ = {'schema': 'hotel'}
    
    service_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    bookings = db.relationship('BookingService', backref='service', lazy=True)
    
    def to_dict(self):
        return {
            'service_id': self.service_id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else None,
            'is_active': self.is_active
        }

class BookingService(db.Model):
    __tablename__ = 'booking_services'
    __table_args__ = {'schema': 'hotel'}
    
    booking_service_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('hotel.bookings.booking_id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('hotel.services.service_id'), nullable=False)
    quantity = db.Column(db.SmallInteger, nullable=False, default=1)
    service_date = db.Column(db.Date, default=datetime.utcnow().date())
    notes = db.Column(db.Text)
    
    def to_dict(self):
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
    __tablename__ = 'payments'
    __table_args__ = {'schema': 'hotel'}
    
    payment_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('hotel.bookings.booking_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    method = db.Column(payment_method, nullable=False)
    status = db.Column(payment_status, default='pending')
    transaction_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def to_dict(self):
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
    __tablename__ = 'cleaning_schedule'
    __table_args__ = {'schema': 'hotel'}
    
    id = db.Column(db.Integer, primary_key=True)
    needs_cleaning = db.Column(db.Boolean, default=False)
    next_cleaning_date = db.Column(db.Date)
    room_id = db.Column(db.Integer, db.ForeignKey('hotel.rooms.room_id'), unique=True, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'needs_cleaning': self.needs_cleaning,
            'next_cleaning_date': self.next_cleaning_date.isoformat() if self.next_cleaning_date else None,
            'room_id': self.room_id,
            'room_number': self.room.room_number if self.room else None
        }