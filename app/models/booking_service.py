from . import db

class BookingService(db.Model):
    __tablename__ = "booking_services"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)

    booking = db.relationship("Booking", back_populates="services")
    service = db.relationship("Service", back_populates="bookings")

    def __repr__(self):
        return f"<BookingService Booking={self.booking_id} Service={self.service_id}>"
