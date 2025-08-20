from flask import Blueprint, request, jsonify
from app.services.guest_service import GuestService

guests_bp = Blueprint("guests", __name__)
guest_service = GuestService()

@guests_bp.route("/", methods=["GET"])
def get_all_guests():
    guests = guest_service.get_all_guests()
    return jsonify([guest.to_dict() for guest in guests])

@guests_bp.route("/<int:guest_id>", methods=["GET"])
def get_guest(guest_id):
    guest = guest_service.get_guest_by_id(guest_id)
    if not guest:
        return jsonify({"error": "Guest not found"}), 404
    return jsonify(guest.to_dict())

@guests_bp.route("/", methods=["POST"])
def create_guest():
    data = request.json
    new_guest = guest_service.create_guest(data)
    return jsonify(new_guest.to_dict()), 201

@guests_bp.route("/<int:guest_id>", methods=["PUT"])
def update_guest(guest_id):
    data = request.json
    updated_guest = guest_service.update_guest(guest_id, data)
    if not updated_guest:
        return jsonify({"error": "Guest not found"}), 404
    return jsonify(updated_guest.to_dict())

@guests_bp.route("/<int:guest_id>", methods=["DELETE"])
def delete_guest(guest_id):
    success = guest_service.delete_guest(guest_id)
    if not success:
        return jsonify({"error": "Guest not found"}), 404
    return jsonify({"message": "Guest deleted"})
