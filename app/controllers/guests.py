from flask import Blueprint, request
from app.services.guest_service import GuestService
from app.utils.responses import json_response

guests_bp = Blueprint('guests', __name__)

@guests_bp.route('', methods=['GET'])
def get_guests():
    try:
        guests = GuestService.get_all_guests()
        return json_response(data=[guest.to_dict() for guest in guests])
    except Exception as e:
        return json_response(message=str(e), status=500)

@guests_bp.route('', methods=['POST'])
def add_guest():
    try:
        data = request.get_json()
        guest = GuestService.create_guest(data)
        return json_response(data=guest.to_dict(), status=201)
    except ValueError as e:
        return json_response(message=str(e), status=400)
    except Exception as e:
        return json_response(message="Internal server error", status=500)