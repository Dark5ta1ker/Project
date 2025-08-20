from flask import Blueprint, request, jsonify
from app.services.room_service import RoomService

rooms_bp = Blueprint("rooms", __name__)
room_service = RoomService()

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
