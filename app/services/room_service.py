from datetime import datetime
from app.models import db, Room, Booking
from app.utils.input_validator import InputValidator

class RoomService:
    @staticmethod
    def get_room_by_number(room_number):
        """Получение комнаты по номеру"""
        return Room.query.filter_by(room_number=room_number).first()

    @staticmethod
    def get_filtered_rooms(status=None, capacity=None, min_capacity=None, check_in=None, check_out=None):
        """Фильтрация комнат с учётом бронирований"""
        query = Room.query
        
        if capacity:
            query = query.filter(Room.capacity == capacity)
        elif min_capacity:
            query = query.filter(Room.capacity >= min_capacity)
            
        if check_in and check_out:
            try:
                check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
                check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
                
                booked_rooms = db.session.query(Booking.room_id).filter(
                    Booking.check_in_date <= check_out_date,
                    Booking.check_out_date >= check_in_date,
                    Booking.status != 'cancelled'
                ).subquery()
                
                if status == "available":
                    query = query.filter(~Room.room_id.in_(booked_rooms))
                elif status == "occupied":
                    query = query.filter(Room.room_id.in_(booked_rooms))
            except ValueError:
                raise ValueError("Invalid date format")

        return query.all()

    @staticmethod
    def create_room(data):
        """Создание комнаты с валидацией"""
        clean_data = InputValidator.sanitize_input(data)
        
        required_fields = ['room_number', 'type', 'capacity', 'daily_rate']
        if not all(field in clean_data for field in required_fields):
            raise ValueError("Missing required fields")

        room = Room(**clean_data)
        db.session.add(room)
        db.session.commit()
        return room