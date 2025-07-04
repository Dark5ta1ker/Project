from flask import Flask, jsonify, request

app = Flask(__name__)

# Пример данных (в реальном проекте используйте базу данных)
rooms = [
    {"id": 1, "number": "101", "type": "Single", "available": True},
    {"id": 2, "number": "102", "type": "Double", "available": False},
]

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    """Возвращает список всех номеров."""
    return jsonify(rooms)

@app.route('/api/rooms', methods=['POST'])
def add_room():
    """Добавляет новый номер."""
    data = request.json
    if not data or 'number' not in data or 'type' not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_room = {
        "id": len(rooms) + 1,
        "number": data["number"],
        "type": data["type"],
        "available": data.get("available", True),
    }
    rooms.append(new_room)
    return jsonify(new_room), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)