from datetime import datetime
from . import db

class Payment(db.Model):
    __tablename__ = "payments"

    payment_id      = db.Column(db.Integer, primary_key=True)
    booking_id      = db.Column(db.Integer, db.ForeignKey("bookings.booking_id"), nullable=False)
    amount          = db.Column(db.Numeric(10, 2), nullable=False)
    method          = db.Column(db.Enum("cash", "credit_card", "online", "bank_transfer", name="payment_method"), nullable=False)
    status          = db.Column(db.Enum("pending", "completed", "failed", "refunded", name="payment_status"), default="pending")
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes           = db.Column(db.Text)

    booking = db.relationship("Booking", back_populates="payments")

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "booking_id": self.booking_id,
            "amount": float(self.amount) if self.amount else None,
            "method": self.method,
            "status": self.status,
            "transaction_date": self.transaction_date.isoformat() if self.transaction_date else None,
            "notes": self.notes,
        }

    def __repr__(self):
        return f"<Payment {self.amount} via {self.method}>"