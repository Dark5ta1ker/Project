from datetime import datetime
from . import db

class BookingService(db.Model):
    __tablename__ = "booking_services"

    booking_service_id = db.Column(db.Integer, primary_key=True)
    booking_id         = db.Column(db.Integer, db.ForeignKey("bookings.booking_id"), nullable=False)
    service_id         = db.Column(db.Integer, db.ForeignKey("services.service_id"), nullable=False)
    quantity           = db.Column(db.SmallInteger, default=1, nullable=False)
    service_date       = db.Column(db.Date, default=datetime.utcnow)
    notes              = db.Column(db.Text)

    booking = db.relationship("Booking", back_populates="services")
    service = db.relationship("Service", back_populates="booking_services")

    def to_dict(self):
        return {
            "booking_service_id": self.booking_service_id,
            "booking_id": self.booking_id,
            "service_id": self.service_id,
            "quantity": self.quantity,
            "service_date": str(self.service_date),
            "notes": self.notes,
        }

    def __repr__(self):
        return f"<BookingService booking={self.booking_id} service={self.service_id}>"