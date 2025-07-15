from app.models import db, Guest
from app.utils.input_validator import InputValidator

class GuestService:
    @staticmethod
    def get_all_guests():
        """Получение всех гостей"""
        return Guest.query.all()

    @staticmethod
    def get_guest_by_id(guest_id):
        """Получение гостя по ID"""
        return db.session.get(Guest, guest_id)

    @staticmethod
    def create_guest(data):
        """Создание нового гостя с валидацией"""
        clean_data = InputValidator.sanitize_input(data)
        
        # Проверка обязательных полей
        required_fields = ['passport_number', 'first_name', 'last_name', 'phone']
        if not all(field in clean_data for field in required_fields):
            raise ValueError("Missing required fields")

        if not InputValidator.validate_phone(clean_data['phone']):
            raise ValueError("Invalid phone format")

        guest = Guest(
            passport_number=clean_data['passport_number'],
            first_name=clean_data['first_name'],
            last_name=clean_data['last_name'],
            phone=clean_data['phone'],
            email=clean_data.get('email'),
            address=clean_data.get('address')
        )
        db.session.add(guest)
        db.session.commit()
        return guest