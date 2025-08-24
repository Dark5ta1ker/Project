from datetime import datetime
from . import db

class Booking(db.Model):
    __tablename__ = "bookings"

    booking_id     = db.Column(db.Integer, primary_key=True)
    guest_id       = db.Column(db.Integer, db.ForeignKey("guests.guest_id"), nullable=False)
    room_id        = db.Column(db.Integer, db.ForeignKey("rooms.room_id"), nullable=False)
    check_in_date  = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    status         = db.Column(db.Enum("confirmed", "cancelled", "checked_in", "checked_out", name="booking_status"), default="confirmed")
    adults         = db.Column(db.SmallInteger, default=1)
    children       = db.Column(db.SmallInteger, default=0)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)

    guest    = db.relationship("Guest", back_populates="bookings")
    room     = db.relationship("Room", back_populates="bookings")
    services = db.relationship("BookingService", back_populates="booking", cascade="all, delete-orphan")
    payments = db.relationship("Payment", back_populates="booking", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "guest_id": self.guest_id,
            "room_id": self.room_id,
            "check_in_date": str(self.check_in_date),
            "check_out_date": str(self.check_out_date),
            "status": self.status,
            "adults": self.adults,
            "children": self.children,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Booking {self.booking_id}>"