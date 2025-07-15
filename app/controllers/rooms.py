from flask import Blueprint, request
from app.services.room_service import RoomService
from app.utils.responses import json_response

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('', methods=['GET'])
def get_rooms():
    try:
        rooms = RoomService.get_filtered_rooms(
            status=request.args.get('status'),
            capacity=request.args.get('capacity'),
            min_capacity=request.args.get('min_capacity'),
            check_in=request.args.get('check_in'),
            check_out=request.args.get('check_out')
        )
        return json_response(data=rooms)
    except ValueError as e:
        return json_response(message=str(e), status=400)
    except Exception as e:
        return json_response(message="Internal server error", status=500)

@rooms_bp.route('', methods=['POST'])
def add_room():
    try:
        data = request.get_json()
        room = RoomService.create_room(data)
        return json_response(data=room.to_dict(), status=201)
    except ValueError as e:
        return json_response(message=str(e), status=400)
    except Exception as e:
        return json_response(message="Internal server error", status=500)

@rooms_bp.route('/<room_number>/full-info', methods=['GET'])
def get_full_room_info(room_number):
    try:
        room_info = RoomService.get_full_room_info(room_number)
        return json_response(data=room_info)
    except Exception as e:
        return json_response(message=str(e), status=500)