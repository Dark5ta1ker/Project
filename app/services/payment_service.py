from app.models.payment import Payment
from app.extensions import db

class PaymentService:
    @staticmethod
    def get_all_payments():
        return Payment.query.all()

    @staticmethod
    def get_payment_by_id(payment_id: int):
        return Payment.query.get_or_404(payment_id)

    @staticmethod
    def create_payment(data: dict):
        payment = Payment(**data)
        db.session.add(payment)
        db.session.commit()
        return payment

    @staticmethod
    def update_payment(payment_id: int, data: dict):
        payment = Payment.query.get_or_404(payment_id)
        for k, v in data.items():
            setattr(payment, k, v)
        db.session.commit()
        return payment

    @staticmethod
    def delete_payment(payment_id: int):
        payment = Payment.query.get_or_404(payment_id)
        db.session.delete(payment)
        db.session.commit()