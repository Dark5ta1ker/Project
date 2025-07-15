from app.models import db, Service, BookingService
from datetime import datetime
from app.utils.input_validator import InputValidator

class ServiceService:
    @staticmethod
    def get_services_by_date_range(start_date, end_date):
        """Получение услуг за период"""
        return (
            db.session.query(BookingService, Service)
            .join(Service)
            .filter(
                BookingService.service_date >= start_date,
                BookingService.service_date <= end_date
            )
            .all()
        )

    @staticmethod
    def create_service(data):
        """Создание новой услуги"""
        clean_data = InputValidator.sanitize_input(data)
        
        if not all(field in clean_data for field in ['name', 'price']):
            raise ValueError("Missing required fields")
        
        service = Service(
            name=clean_data['name'],
            description=clean_data.get('description'),
            price=clean_data['price'],
            is_active=clean_data.get('is_active', True)
        )
        
        db.session.add(service)
        db.session.commit()
        return service