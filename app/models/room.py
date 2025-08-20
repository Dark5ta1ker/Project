from . import db

class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price_per_night = db.Column(db.Numeric(10, 2), nullable=False)

    bookings = db.relationship("Booking", back_populates="room", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Room {self.number} ({self.room_type})>"
