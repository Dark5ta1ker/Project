from datetime import datetime
from . import db

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    guest = db.relationship("Guest", back_populates="bookings")
    room = db.relationship("Room", back_populates="bookings")
    services = db.relationship("BookingService", back_populates="booking", cascade="all, delete-orphan")
    payments = db.relationship("Payment", back_populates="booking", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Booking {self.id} Guest={self.guest_id} Room={self.room_id}>"
