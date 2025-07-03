from flask import Flask, jsonify, request

app = Flask(__name__)

# Пример данных (в реальном проекте используйте базу данных)
rooms = [
    {"id": 1, "number": "101", "type": "Single", "available": True},
    {"id": 2, "number": "102", "type": "Double", "available": False},
]

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    return jsonify(rooms)

@app.route('/api/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    room = next((r for r in rooms if r["id"] == room_id), None)
    if room:
        return jsonify(room)
    return jsonify({"error": "Room not found"}), 404

@app.route('/api/rooms', methods=['POST'])
def add_room():
    data = request.json
    new_room = {
        "id": len(rooms) + 1,
        "number": data.get("number"),
        "type": data.get("type"),
        "available": data.get("available", True),
    }
    rooms.append(new_room)
    return jsonify(new_room), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)