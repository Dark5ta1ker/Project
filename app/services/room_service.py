from app.models.room import Room
from app.models.booking import Booking
from app.extensions import db
from datetime import datetime
from app.models.payment import Payment
from app.models.booking_service import BookingService

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

    @staticmethod
    def get_rooms_with_filters(status=None, capacity=None, min_capacity=None, check_in=None, check_out=None):

        query = Room.query
        rooms = query.all()

        result = []
        for room in rooms:
            dynamic_status = "available"

            # Проверка занятости по датам
            if check_in and check_out:
                overlapping = Booking.query.filter(
                    Booking.room_id == room.room_id,
                    Booking.check_in_date < check_out,
                    Booking.check_out_date > check_in
                ).first()
                if overlapping:
                    dynamic_status = "occupied"

            # Проверка обслуживания
            if getattr(room, "status", None) == "maintenance":
                dynamic_status = "maintenance"

            # Фильтр по статусу
            if status and dynamic_status != status:
                continue

            # Фильтр по capacity
            if capacity:
                try:
                    cap_int = int(capacity)
                except ValueError:
                    cap_int = None
                if cap_int is not None and room.capacity != cap_int:
                    continue

            # Фильтр по min_capacity
            if min_capacity:
                try:
                    min_cap_int = int(min_capacity)
                except ValueError:
                    min_cap_int = None
                if min_cap_int is not None and room.capacity < min_cap_int:
                    continue

            result.append({
                **room.to_dict(),
                "dynamic_status": dynamic_status
            })

        return result

    @staticmethod
    def get_room_full_info(room_number: str):
        room_number = str(room_number)
        room = Room.query.filter_by(room_number=room_number).first()
        if not room:
            print("Room not found")
            return None

        bookings = [
            {
                "id": b.id,
                "guest_name": b.guest.name if b.guest else "N/A",
                "check_in": str(b.check_in_date),
                "check_out": str(b.check_out_date),
                "status": b.status,
            }
            for b in Booking.query.filter_by(room_id=room.room_number).all()
        ]

        payments = [
            {
                "id": p.id,
                "date": str(p.date),
                "amount": float(p.amount),
                "status": p.status,
                "method": p.method,
            }
            for p in Payment.query.join(Booking).filter(Booking.room_id == room.room_number).all()
        ]

        services = [
            {
                "id": s.id,
                "date": str(s.date),
                "service_name": s.service_name,
                "quantity": s.quantity,
                "notes": s.notes,
            }
            for s in BookingService.query.join(Booking).filter(Booking.room_id == room.room_number).all()
        ]

        return {
            "room_info": room.to_dict(),
            "bookings": bookings,
            "payments": payments,
            "services": services,
            "cleaning": [],
        }
