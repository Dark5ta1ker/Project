from . import db

class Service(db.Model):
    __tablename__ = "services"

    service_id  = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price       = db.Column(db.Numeric(10, 2), nullable=False)
    is_active   = db.Column(db.Boolean, default=True)

    booking_services = db.relationship("BookingService", back_populates="service")

    def to_dict(self):
        return {
            "service_id": self.service_id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price) if self.price else None,
            "is_active": self.is_active,
        }

    def __repr__(self):
        return f"<Service {self.name}>"