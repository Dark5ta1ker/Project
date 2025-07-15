from flask import Blueprint, request
from app.services.cleaning_service import CleaningService
from app.utils.responses import json_response

cleaning_bp = Blueprint('cleaning', __name__)

@cleaning_bp.route('', methods=['GET'])
def get_cleaning_schedule():
    try:
        schedules = CleaningService.get_all_schedules()
        return json_response(data=[s.to_dict() for s in schedules])
    except Exception as e:
        return json_response(message="Internal server error", status=500)

@cleaning_bp.route('', methods=['POST'])
def add_cleaning_schedule():
    try:
        data = request.get_json()
        schedule = CleaningService.create_schedule(data)
        return json_response(data=schedule.to_dict(), status=201)
    except ValueError as e:
        return json_response(message=str(e), status=400)
    except Exception as e:
        return json_response(message="Internal server error", status=500)

@cleaning_bp.route('', methods=['PUT'])
def update_cleaning_schedule():
    try:
        data = request.get_json()
        schedule = CleaningService.update_schedule(data)
        return json_response(data=schedule.to_dict())
    except ValueError as e:
        return json_response(message=str(e), status=400)
    except Exception as e:
        return json_response(message="Internal server error", status=500)