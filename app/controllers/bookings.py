from flask import Blueprint, request
from app.services.booking_service import BookingService
from app.utils.responses import json_response

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('', methods=['GET'])
def get_bookings():
    try:
        bookings = BookingService.get_all_bookings()
        return json_response(data=[b.to_dict() for b in bookings])
    except Exception as e:
        return json_response(message="Internal server error", status=500)

@bookings_bp.route('', methods=['POST'])
def add_booking():
    try:
        data = request.get_json()
        booking = BookingService.create_booking(data)
        return json_response(data=booking.to_dict(), status=201)
    except ValueError as e:
        return json_response(message=str(e), status=400)
    except Exception as e:
        return json_response(message="Internal server error", status=500)