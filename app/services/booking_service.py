from datetime import datetime
from app.models import db, Booking, Guest, Room
from app.utils.input_validator import InputValidator
from app.services.guest_service import GuestService

class BookingService:
    @staticmethod
    def create_booking(data):
        """Создание бронирования с комплексной проверкой"""
        clean_data = InputValidator.sanitize_input(data)
        
        # Валидация обязательных полей
        required_fields = ['room_id', 'check_in_date', 'check_out_date', 'guest']
        if not all(field in clean_data for field in required_fields):
            raise ValueError("Missing required fields")

        # Проверка дат
        try:
            check_in = datetime.strptime(clean_data['check_in_date'], "%Y-%m-%d").date()
            check_out = datetime.strptime(clean_data['check_out_date'], "%Y-%m-%d").date()
            if check_out <= check_in:
                raise ValueError("Check-out date must be after check-in date")
        except ValueError:
            raise ValueError("Invalid date format")

        # Проверка комнаты
        room = db.session.get(Room, clean_data['room_id'])
        if not room or room.status != 'available':
            raise ValueError("Room not available")

        # Проверка гостя
        guest_data = clean_data['guest']
        guest = Guest.query.filter_by(passport_number=guest_data['passport_number'].upper()).first()
        if not guest:
            guest = GuestService.create_guest(guest_data)

        # Проверка доступности комнаты
        conflicting_booking = Booking.query.filter(
            Booking.room_id == clean_data['room_id'],
            Booking.check_in_date <= check_out,
            Booking.check_out_date >= check_in,
            Booking.status != 'cancelled'
        ).first()
        
        if conflicting_booking:
            raise ValueError("Room already booked for selected dates")

        # Создание бронирования
        booking = Booking(
            guest_id=guest.guest_id,
            room_id=clean_data['room_id'],
            check_in_date=check_in,
            check_out_date=check_out,
            adults=clean_data.get('adults', 1),
            children=clean_data.get('children', 0),
            status='confirmed'
        )
        
        db.session.add(booking)
        room.status = 'occupied'
        db.session.commit()
        return booking