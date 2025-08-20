from datetime import datetime
from . import db

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    method = db.Column(db.String(50), nullable=False)  # "cash", "card" и т.д.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    booking = db.relationship("Booking", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.amount} via {self.method}>"
