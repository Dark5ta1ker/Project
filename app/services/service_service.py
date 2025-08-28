from app.models.service import Service
from app.extensions import db
from datetime import datetime
from app.models.booking_service import BookingService

class ServiceService:
    @staticmethod
    def get_all_services():
        return Service.query.all()

    @staticmethod
    def get_service_by_id(service_id: int):
        return Service.query.get_or_404(service_id)

    @staticmethod
    def create_service(data: dict):
        service = Service(**data)
        db.session.add(service)
        db.session.commit()
        return service

    @staticmethod
    def update_service(service_id: int, data: dict):
        service = Service.query.get_or_404(service_id)
        for k, v in data.items():
            setattr(service, k, v)
        db.session.commit()
        return service

    @staticmethod
    def delete_service(service_id: int):
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()

    @staticmethod
    def get_services_by_date(start_date, end_date):
        results = (
            db.session.query(BookingService, Service)
            .join(Service, BookingService.service_id == Service.service_id)
            .filter(BookingService.service_date.between(start_date, end_date))
            .all()
        )
        return [
            {
                "booking_service_id": b.booking_service_id,
                "booking_id": b.booking_id,
                "service_date": b.service_date.isoformat(),
                "quantity": b.quantity,
                "notes": b.notes,
                "service": {
                    "id": s.service_id,
                    "name": s.name,
                    "description": s.description,
                    "price": str(s.price),
                },
            }
            for b, s in results
        ]
