from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from app.error_handlers import register_error_handlers
from app.logger_config import setup_logger  # Импортируем настройку логгера

# Настройка логгера
logger = setup_logger()

# Загрузка переменных окружения из .env
load_dotenv()

# Получение переменных окружения
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

app = Flask(__name__)

# Настройка подключения к PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель для номеров
class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    available = db.Column(db.Boolean, default=True)

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{
        "id": room.id,
        "number": room.number,
        "type": room.type,
        "available": room.available
    } for room in rooms])

@app.route('/api/rooms', methods=['POST'])
def add_room():
    data = request.json
    if not data or 'number' not in data or 'type' not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_room = Room(
        number=data["number"],
        type=data["type"],
        available=data.get("available", True)
    )
    db.session.add(new_room)
    db.session.commit()

    return jsonify({
        "id": new_room.id,
        "number": new_room.number,
        "type": new_room.type,
        "available": new_room.available
    }), 201

# Регистрация обработчиков ошибок
register_error_handlers(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц, если их нет
    app.run(host='0.0.0.0', port=5000)