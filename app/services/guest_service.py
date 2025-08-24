from app.models.guest import Guest
from app.extensions import db

class GuestService:
    @staticmethod
    def get_all_guests():
        return Guest.query.all()

    @staticmethod
    def get_guest_by_id(guest_id: int):
        return Guest.query.get_or_404(guest_id)

    @staticmethod
    def create_guest(data: dict):
        guest = Guest(**data)
        db.session.add(guest)
        db.session.commit()
        return guest

    @staticmethod
    def update_guest(guest_id: int, data: dict):
        guest = Guest.query.get_or_404(guest_id)
        for k, v in data.items():
            setattr(guest, k, v)
        db.session.commit()
        return guest

    @staticmethod
    def delete_guest(guest_id: int):
        guest = Guest.query.get_or_404(guest_id)
        db.session.delete(guest)
        db.session.commit()