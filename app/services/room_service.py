from app.models.room import Room
from app.extensions import db

class RoomService:
    @staticmethod
    def get_all_rooms():
        return Room.query.all()

    @staticmethod
    def get_room_by_id(room_id: int):
        return Room.query.get_or_404(room_id)

    @staticmethod
    def create_room(data: dict):
        room = Room(**data)
        db.session.add(room)
        db.session.commit()
        return room

    @staticmethod
    def update_room(room_id: int, data: dict):
        room = Room.query.get_or_404(room_id)
        for k, v in data.items():
            setattr(room, k, v)
        db.session.commit()
        return room

    @staticmethod
    def delete_room(room_id: int):
        room = Room.query.get_or_404(room_id)
        db.session.delete(room)
        db.session.commit()