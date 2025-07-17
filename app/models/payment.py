from . import db
from datetime import datetime
from .base import payment_method, payment_status

class Payment(db.Model):
    """
    Модель для хранения информации о платежах.
    Таблица: payments (схема hotel).
    """
    __tablename__ = 'payments'
    __table_args__ = {'schema': 'hotel'}
    
    payment_id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
    booking_id = db.Column(db.Integer, db.ForeignKey('hotel.bookings.booking_id'), nullable=False)  # Внешний ключ на bookings
    amount = db.Column(db.Numeric(10, 2), nullable=False)  # Сумма платежа
    method = db.Column(payment_method, nullable=False)  # Метод оплаты
    status = db.Column(payment_status, default='pending')  # Статус платежа
    transaction_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)  # Дата транзакции
    notes = db.Column(db.Text)  # Примечания (необязательно)
    
    def to_dict(self):
        """
        Преобразует объект Payment в словарь для сериализации в JSON.
        """
        return {
            'payment_id': self.payment_id,
            'booking_id': self.booking_id,
            'amount': float(self.amount) if self.amount else None,
            'method': self.method,
            'status': self.status,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'notes': self.notes
        }