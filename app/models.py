from app import db
from datetime import datetime

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False, unique=True)
    type = db.Column(db.String(10), default='Standart')
    capacity = db.Column(db.Integer, default=2)
    available = db.Column(db.Boolean, default=True)

    # Метод для преобразования объекта в словарь
    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'type': self.type,
            'capacity': self.capacity,
            'available': self.available
        }

class CleaningSchedule(db.Model):
    __tablename__ = 'cleaning_schedule'
    id = db.Column(db.Integer, primary_key=True)
    needs_cleaning = db.Column(db.Boolean, default=False)
    next_cleaning_date = db.Column(db.Date, nullable=True)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'needs_cleaning': self.needs_cleaning,
            'next_cleaning_date': self.next_cleaning_date.isoformat() if self.next_cleaning_date else None,
            'room_id': self.room_id
        }

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(100), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'guest_name': self.guest_name,
            'check_in_date': self.check_in_date.isoformat(),
            'check_out_date': self.check_out_date.isoformat(),
            'room_id': self.room_id
        }