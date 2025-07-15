from flask import Blueprint, request
from app.services.room_service import RoomService
from app.utils.responses import json_response

ui_bp = Blueprint('ui', __name__)

@ui_bp.route('/rooms', methods=['GET'])
def ui_get_rooms():
    try:
        rooms = RoomService.get_filtered_rooms(
            status=request.args.get('status'),
            check_in=request.args.get('check_in'),
            check_out=request.args.get('check_out')
        )
        return json_response(data=rooms)
    except Exception as e:
        return json_response(message=str(e), status=500)