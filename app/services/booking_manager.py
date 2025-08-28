from app.models.booking import Booking
from app.extensions import db

class BookingManager:
    @staticmethod
    def get_all_bookings():
        return Booking.query.all()

    @staticmethod
    def get_booking_by_id(bk_s_id: int):
        return Booking.query.get_or_404(bk_s_id)

    @staticmethod
    def create_booking(data: dict):
        bs = Booking(**data)
        db.session.add(bs)
        db.session.commit()
        return bs

    @staticmethod
    def update_booking(bk_s_id: int, data: dict):
        bs = Booking.query.get_or_404(bk_s_id)
        for k, v in data.items():
            setattr(bs, k, v)
        db.session.commit()
        return bs

    @staticmethod
    def delete_booking(bk_s_id: int):
        bs = Booking.query.get_or_404(bk_s_id)
        db.session.delete(bs)
        db.session.commit()