from flask import Blueprint, request, jsonify
from app.services import BookingServices

booking_services_bp = Blueprint("booking_services", __name__)
booking_services = BookingServices()

@booking_services_bp.route("/", methods=["GET"])
def get_all_booking_service():
    services = booking_services.get_all_booking_service()
    return jsonify([s.to_dict() for s in services])

@booking_services_bp.route("/<int:bs_id>", methods=["GET"])
def get_booking_service(bs_id):
    service = booking_services.get_booking_service(bs_id)
    return jsonify(service.to_dict())

@booking_services_bp.route("/", methods=["POST"])
def create_booking_service():
    data = request.json
    new_service = booking_services.create_booking_service(data)
    return jsonify(new_service.to_dict()), 201

@booking_services_bp.route("/<int:bs_id>", methods=["PUT"])
def update_booking_service(bs_id):
    data = request.json
    updated_service = booking_services.update_booking_service(bs_id, data)
    return jsonify(updated_service.to_dict())

@booking_services_bp.route("/<int:bs_id>", methods=["DELETE"])
def delete_booking_service(bs_id):
    booking_services.delete_booking_service(bs_id)
    return jsonify({"message": "Booking service deleted"})