from app.models.service import Service
from app.extensions import db

class ServiceService:
    @staticmethod
    def get_all():
        return Service.query.all()

    @staticmethod
    def get_by_id(service_id: int):
        return Service.query.get_or_404(service_id)

    @staticmethod
    def create(data: dict):
        service = Service(**data)
        db.session.add(service)
        db.session.commit()
        return service

    @staticmethod
    def update(service_id: int, data: dict):
        service = Service.query.get_or_404(service_id)
        for key, value in data.items():
            setattr(service, key, value)
        db.session.commit()
        return service

    @staticmethod
    def delete(service_id: int):
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
