from flask import Blueprint, request, jsonify
from app.services import BookingManager

bookings_bp = Blueprint("bookings", __name__)
booking_service = BookingManager()

@bookings_bp.route("/", methods=["GET"])
def get_all_bookings():
    bookings = booking_service.get_all_bookings()
    return jsonify([booking.to_dict() for booking in bookings])

@bookings_bp.route("/<int:booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = booking_service.get_booking_by_id(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify(booking.to_dict())

@bookings_bp.route("/", methods=["POST"])
def create_booking():
    data = request.json
    new_booking = booking_service.create_booking(data)
    return jsonify(new_booking.to_dict()), 201

@bookings_bp.route("/<int:booking_id>", methods=["PUT"])
def update_booking(booking_id):
    data = request.json
    updated_booking = booking_service.update_booking(booking_id, data)
    if not updated_booking:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify(updated_booking.to_dict())

@bookings_bp.route("/<int:booking_id>", methods=["DELETE"])
def delete_booking(booking_id):
    success = booking_service.delete_booking(booking_id)
    if not success:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify({"message": "Booking deleted"})
