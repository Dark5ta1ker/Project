from datetime import datetime
from . import db

class Guest(db.Model):
    __tablename__ = "guests"

    guest_id        = db.Column(db.Integer, primary_key=True)
    passport_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name      = db.Column(db.String(50), nullable=False)
    last_name       = db.Column(db.String(50), nullable=False)
    phone           = db.Column(db.String(20), nullable=False)
    email           = db.Column(db.String(100))
    address         = db.Column(db.Text)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bookings = db.relationship("Booking", back_populates="guest", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "guest_id": self.guest_id,
            "passport_number": self.passport_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Guest {self.first_name} {self.last_name}>"