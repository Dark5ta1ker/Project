from flask import Blueprint, request, jsonify
from app.services import RoomService, BookingService

rooms_bp = Blueprint("rooms", __name__)
room_service = RoomService()
booking_service = BookingService()

@rooms_bp.route("/", methods=["GET"])
def get_all_rooms():
    rooms = room_service.get_all_rooms()
    return jsonify([room.to_dict() for room in rooms])

@rooms_bp.route("/<int:room_id>", methods=["GET"])
def get_room(room_id):
    room = room_service.get_room_by_id(room_id)
    if not room:
        return jsonify({"error": "Room not found"}), 404
    return jsonify(room.to_dict())

@rooms_bp.route("/", methods=["POST"])
def create_room():
    data = request.json
    new_room = room_service.create_room(data)
    return jsonify(new_room.to_dict()), 201

@rooms_bp.route("/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    data = request.json
    updated_room = room_service.update_room(room_id, data)
    if not updated_room:
        return jsonify({"error": "Room not found"}), 404
    return jsonify(updated_room.to_dict())

@rooms_bp.route("/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    success = room_service.delete_room(room_id)
    if not success:
        return jsonify({"error": "Room not found"}), 404
    return jsonify({"message": "Room deleted"})

@rooms_bp.route("/search", methods=["GET"])
def search_rooms():
    check_in = request.args.get("check_in")
    check_out = request.args.get("check_out")
    status = request.args.get("status")  # "available" | "occupied" | "maintenance"
    capacity = request.args.get("capacity")
    min_capacity = request.args.get("min_capacity")

    if not check_in or not check_out:
        return jsonify({"error": "check_in и check_out обязательны"}), 400

    rooms = room_service.get_rooms_with_filters(
        check_in=check_in,
        check_out=check_out,
        status=status if status else None,
        capacity=int(capacity) if capacity else None,
        min_capacity=int(min_capacity) if min_capacity else None
    )
    return jsonify(rooms)

@rooms_bp.route("/<int:room_number>/full-info", methods=["GET"])
def get_room_full_info(room_number):
    data = room_service.get_room_full_info(room_number)
    if not data:
        return jsonify({"error": "Room not found"}), 404
    return jsonify(data)

