from app.models.booking_service import BookingService
from app.extensions import db

class BookingServices:
    @staticmethod
    def get_all_booking_service():
        return BookingService.query.all()

    @staticmethod
    def get_booking_service(bs_id: int):
        return BookingService.query.get_or_404(bs_id)

    @staticmethod
    def create_booking_service(data: dict):
        bs = BookingService(**data)
        db.session.add(bs)
        db.session.commit()
        return bs

    @staticmethod
    def update_booking_service(bs_id: int, data: dict):
        bs = BookingService.query.get_or_404(bs_id)
        for key, value in data.items():
            setattr(bs, key, value)
        db.session.commit()
        return bs

    @staticmethod
    def delete_booking_service(bs_id: int):
        bs = BookingService.query.get_or_404(bs_id)
        db.session.delete(bs)
        db.session.commit()