from app.models.booking import Booking
from app.extensions import db

class BookingService:
    @staticmethod
    def get_all():
        return Booking.query.all()

    @staticmethod
    def get_by_id(booking_id: int):
        return Booking.query.get_or_404(booking_id)

    @staticmethod
    def create(data: dict):
        booking = Booking(**data)
        db.session.add(booking)
        db.session.commit()
        return booking

    @staticmethod
    def update(booking_id: int, data: dict):
        booking = Booking.query.get_or_404(booking_id)
        for key, value in data.items():
            setattr(booking, key, value)
        db.session.commit()
        return booking

    @staticmethod
    def delete(booking_id: int):
        booking = Booking.query.get_or_404(booking_id)
        db.session.delete(booking)
        db.session.commit()
