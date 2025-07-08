from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from app.error_handlers import register_error_handlers  # Абсолютный импорт
from app.logger_config import setup_logger

app = Flask(__name__)

# Настройка подключения к PostgreSQL
DB_HOST = 'db'
DB_NAME = 'hotel_db'
DB_USER = 'hotel_user'
DB_PASSWORD = 'hotel_password'

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
    """Возвращает список всех номеров."""
    rooms = Room.query.all()
    return jsonify([{
        "id": room.id,
        "number": room.number,
        "type": room.type,
        "available": room.available
    } for room in rooms])

@app.route('/api/rooms', methods=['POST'])
def add_room():
    """Добавляет новый номер."""
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)