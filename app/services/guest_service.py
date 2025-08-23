from app.models.guest import Guest
from app.extensions import db

class GuestService:
    @staticmethod
    def get_all_guests():
        return Guest.query.all()

    @staticmethod
    def get_by_id(guest_id: int):
        return Guest.query.get_or_404(guest_id)

    @staticmethod
    def create(data: dict):
        guest = Guest(**data)
        db.session.add(guest)
        db.session.commit()
        return guest

    @staticmethod
    def update(guest_id: int, data: dict):
        guest = Guest.query.get_or_404(guest_id)
        for key, value in data.items():
            setattr(guest, key, value)
        db.session.commit()
        return guest

    @staticmethod
    def delete(guest_id: int):
        guest = Guest.query.get_or_404(guest_id)
        db.session.delete(guest)
        db.session.commit()
