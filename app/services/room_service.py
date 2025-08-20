from app.models.room import Room
from app.extensions import db

class RoomService:
    @staticmethod
    def get_all():
        return Room.query.all()

    @staticmethod
    def get_by_id(room_id: int):
        return Room.query.get_or_404(room_id)

    @staticmethod
    def create(data: dict):
        room = Room(**data)
        db.session.add(room)
        db.session.commit()
        return room

    @staticmethod
    def update(room_id: int, data: dict):
        room = Room.query.get_or_404(room_id)
        for key, value in data.items():
            setattr(room, key, value)
        db.session.commit()
        return room

    @staticmethod
    def delete(room_id: int):
        room = Room.query.get_or_404(room_id)
        db.session.delete(room)
        db.session.commit()
