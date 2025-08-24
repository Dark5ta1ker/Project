from app.models.service import Service
from app.extensions import db

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