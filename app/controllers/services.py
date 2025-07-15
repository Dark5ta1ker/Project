from flask import Blueprint, request
from app.services.service_service import ServiceService
from app.utils.responses import json_response

services_bp = Blueprint('services', __name__)

@services_bp.route('', methods=['GET'])
def get_services():
    try:
        services = ServiceService.get_active_services()
        return json_response(data=[s.to_dict() for s in services])
    except Exception as e:
        return json_response(message="Internal server error", status=500)

@services_bp.route('', methods=['POST'])
def add_service():
    try:
        data = request.get_json()
        service = ServiceService.create_service(data)
        return json_response(data=service.to_dict(), status=201)
    except ValueError as e:
        return json_response(message=str(e), status=400)
    except Exception as e:
        return json_response(message="Internal server error", status=500)

@services_bp.route('/by-date', methods=['GET'])
def get_services_by_date():
    try:
        services = ServiceService.get_services_by_date_range(
            request.args.get('start_date'),
            request.args.get('end_date')
        )
        return json_response(data=[{
            'date': bs.service_date.strftime('%d.%m.%Y'),
            'room_number': room.room_number,
            'service_name': service.name,
            'quantity': bs.quantity,
            'notes': bs.notes or ""
        } for bs, room, service in services])
    except Exception as e:
        return json_response(message=str(e), status=500)