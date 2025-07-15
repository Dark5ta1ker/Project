from app.models import db, Payment, Booking
from app.utils.input_validator import InputValidator

class PaymentService:
    @staticmethod
    def create_payment(data):
        """Создание платежа с проверками"""
        clean_data = InputValidator.sanitize_input(data)
        
        required_fields = ['booking_id', 'amount', 'method']
        if not all(field in clean_data for field in required_fields):
            raise ValueError("Missing required fields")
        
        booking = db.session.get(Booking, clean_data['booking_id'])
        if not booking:
            raise ValueError("Booking not found")
        
        payment = Payment(
            booking_id=clean_data['booking_id'],
            amount=clean_data['amount'],
            method=clean_data['method'],
            status=clean_data.get('status', 'pending'),
            notes=clean_data.get('notes')
        )
        
        db.session.add(payment)
        db.session.commit()
        return payment