from . import db

class Guest(db.Model):
    __tablename__ = "guest"

    id = db.Column(db.Integer, primary_key=True)
    passport_number = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))

    bookings = db.relationship("Booking", back_populates="guest", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Guest {self.first_name} {self.last_name}>"
