from . import db

class Room(db.Model):
    __tablename__ = "rooms"

    room_id     = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(10), unique=True, nullable=False)
    type        = db.Column(db.Enum("Basic", "Advanced", "Business", "Dorm", name="room_type"), nullable=False)
    capacity    = db.Column(db.SmallInteger, nullable=False)
    daily_rate  = db.Column(db.Numeric(10, 2), nullable=False)
    status      = db.Column(db.Enum("available", "occupied", "maintenance", "reserved", name="room_status"), default="available")
    description = db.Column(db.Text)

    bookings = db.relationship("Booking", back_populates="room")

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "room_number": self.room_number,
            "type": self.type,
            "capacity": self.capacity,
            "daily_rate": float(self.daily_rate) if self.daily_rate else None,
            "status": self.status,
            "description": self.description,
        }

    def __repr__(self):
        return f"<Room {self.room_number}>"