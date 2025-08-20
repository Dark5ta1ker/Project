from . import db

class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    bookings = db.relationship("BookingService", back_populates="service", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Service {self.name}>"
