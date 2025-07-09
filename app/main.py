from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from app.error_handlers import register_error_handlers
from app.logger_config import setup_logger  # Импортируем настройку логгера

# Настройка логгера
logger = setup_logger()

# Загрузка переменных окружения из .env
load_dotenv()

app = Flask(__name__)

# Временные данные для тестирования (вместо базы данных)
rooms_data = [
    {"id": 1, "number": "101", "type": "Single", "available": True},
    {"id": 2, "number": "102", "type": "Double", "available": False},
]

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    logger.info("GET request received for /api/rooms")
    try:
        # Временный ответ вместо запроса к базе данных
        return jsonify(rooms_data), 200
    except Exception as e:
        logger.error(f"Error retrieving rooms: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/rooms', methods=['POST'])
def add_room():
    logger.info("POST request received for /api/rooms")
    try:
        data = request.json
        if not data or 'number' not in data or 'type' not in data:
            logger.warning("Invalid data received: %s", data)
            return jsonify({"error": "Invalid data"}), 400

        # Создаем новый номер комнаты (временно в памяти)
        new_room = {
            "id": len(rooms_data) + 1,
            "number": data["number"],
            "type": data["type"],
            "available": data.get("available", True),
        }
        rooms_data.append(new_room)

        logger.info(f"New room added: {new_room['number']}")
        return jsonify(new_room), 201
    except Exception as e:
        logger.error(f"Error adding room: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Регистрация обработчиков ошибок
register_error_handlers(app)

if __name__ == '__main__':
    logger.info("Starting the application...")
    app.run(host='0.0.0.0', port=5000)