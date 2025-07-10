from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from app.logger_config import setup_logger
from app.error_handlers import register_error_handlers
from app.input_validator import InputValidator

# Загрузка переменных окружения из .env
load_dotenv()

# Настройка логгера
logger = setup_logger()

# Создание приложения Flask
app = Flask(__name__)

# Получение переменных окружения для подключения к базе данных
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Настройка подключения к PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# Модель для номеров
class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    available = db.Column(db.Boolean, default=True)

# Маршрут для получения списка комнат
@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    logger.info("GET request received for /api/rooms")
    try:
        rooms = Room.query.all()
        logger.debug(f"Rooms retrieved: {len(rooms)}")
        return jsonify([{
            "id": room.id,
            "number": room.number,
            "type": room.type,
            "available": room.available
        } for room in rooms])
    except Exception as e:
        logger.error(f"Error retrieving rooms: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Маршрут для добавления новой комнаты
@app.route('/api/rooms', methods=['POST'])
def add_room():
    logger.info("POST request received for /api/rooms")
    try:
        data = request.json

        # Проверка входных данных на наличие опасных паттернов
        if not InputValidator.is_safe_input(data):
            logger.warning("Potentially malicious input detected: %s", data)
            return jsonify({"error": "Input contains potentially malicious content"}), 400

        if not data or 'number' not in data or 'type' not in data:
            logger.warning("Invalid data received: %s", data)
            return jsonify({"error": "Invalid data"}), 400

        new_room = Room(
            number=data["number"],
            type=data["type"],
            available=data.get("available", True)
        )
        db.session.add(new_room)
        db.session.commit()

        logger.info(f"New room added: {new_room.number}")
        return jsonify({
            "id": new_room.id,
            "number": new_room.number,
            "type": new_room.type,
            "available": new_room.available
        }), 201
    except Exception as e:
        logger.error(f"Error adding room: {e}")
        return jsonify({"error": "Internal server error"}), 500

# Регистрация обработчиков ошибок
register_error_handlers(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц, если их нет
    app.run(host='0.0.0.0', port=5000)