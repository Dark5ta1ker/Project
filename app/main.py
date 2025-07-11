from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from datetime import datetime
from app.logger_config import setup_logger
from app.error_handlers import register_error_handlers
from app.input_validator import InputValidator
from app.models import db, Room, CleaningSchedule, Booking

# Загрузка переменных окружения
load_dotenv()

# Настройка логгера
logger = setup_logger()

# Создание приложения Flask
app = Flask(__name__)

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных
db.init_app(app)

# Маршруты для работы с комнатами
@app.route('/api/rooms', methods=['GET', 'POST'])
def handle_rooms():
    if request.method == 'GET':
        return get_rooms()
    elif request.method == 'POST':
        return add_room()

def get_rooms():
    """Получение списка комнат с возможностью фильтрации"""
    try:
        # Получаем параметры запроса
        status = request.args.get('status')
        guests = request.args.get('guests', type=int)
        check_in = request.args.get('check_in')
        check_out = request.args.get('check_out')

        query = Room.query

        # Фильтрация по статусу
        if status:
            status = status.lower()
            if status == 'свободен' or status == 'free':
                query = query.filter(Room.available == True)
            elif status == 'занят' or status == 'occupied':
                query = query.filter(Room.available == False)

        # Фильтрация по вместимости
        if guests:
            query = query.filter(Room.capacity >= guests)

        # Фильтрация по датам бронирования
        if check_in and check_out:
            try:
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
                
                # Ищем комнаты без бронирований в указанный период
                query = query.filter(
                    ~Room.id.in_(
                        db.session.query(Booking.room_id).filter(
                            Booking.check_in_date <= check_out_date,
                            Booking.check_out_date >= check_in_date
                        )
                    )
                )
            except ValueError as e:
                logger.warning(f"Invalid date format: {e}")
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        rooms = query.all()
        return jsonify([{
            'id': room.id,
            'number': room.number,
            'type': room.type,
            'capacity': room.capacity,
            'available': room.available,
            'needs_cleaning': room.cleaning_schedule.needs_cleaning if room.cleaning_schedule else False
        } for room in rooms])

    except Exception as e:
        logger.error(f"Error retrieving rooms: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def add_room():
    """Добавление новой комнаты"""
    try:
        data = request.json

        # Валидация входных данных
        if not InputValidator.is_safe_input(data):
            return jsonify({"error": "Invalid input data"}), 400

        required_fields = {'number', 'type', 'capacity'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Создание новой комнаты
        new_room = Room(
            number=data['number'],
            type=data['type'],
            capacity=data['capacity'],
            available=data.get('available', True)
        )

        db.session.add(new_room)
        db.session.commit()

        # Создание расписания уборки для новой комнаты
        cleaning_schedule = CleaningSchedule(
            room_id=new_room.id,
            needs_cleaning=False,
            next_cleaning_date=None
        )
        db.session.add(cleaning_schedule)
        db.session.commit()

        return jsonify({
            'id': new_room.id,
            'number': new_room.number,
            'type': new_room.type,
            'capacity': new_room.capacity,
            'available': new_room.available
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding room: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Маршруты для работы с уборкой
@app.route('/api/cleaning-schedule', methods=['GET', 'POST'])
def handle_cleaning():
    if request.method == 'GET':
        return get_cleaning_schedule()
    elif request.method == 'POST':
        return add_cleaning_schedule()

def get_cleaning_schedule():
    """Получение расписания уборки"""
    try:
        schedules = CleaningSchedule.query.all()
        return jsonify([{
            'id': s.id,
            'room_id': s.room_id,
            'room_number': s.room.number if s.room else None,
            'needs_cleaning': s.needs_cleaning,
            'next_cleaning_date': s.next_cleaning_date.isoformat() if s.next_cleaning_date else None
        } for s in schedules])
    except Exception as e:
        logger.error(f"Error retrieving cleaning schedule: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def add_cleaning_schedule():
    """Добавление записи в расписание уборки"""
    try:
        data = request.json

        if not InputValidator.is_safe_input(data):
            return jsonify({"error": "Invalid input data"}), 400

        required_fields = {'room_id', 'needs_cleaning'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        new_schedule = CleaningSchedule(
            room_id=data['room_id'],
            needs_cleaning=data['needs_cleaning'],
            next_cleaning_date=datetime.strptime(data['next_cleaning_date'], '%Y-%m-%d').date() 
            if 'next_cleaning_date' in data else None
        )

        db.session.add(new_schedule)
        db.session.commit()

        return jsonify({
            'id': new_schedule.id,
            'room_id': new_schedule.room_id,
            'needs_cleaning': new_schedule.needs_cleaning,
            'next_cleaning_date': new_schedule.next_cleaning_date.isoformat() 
            if new_schedule.next_cleaning_date else None
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding cleaning schedule: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Маршруты для работы с бронированиями
@app.route('/api/bookings', methods=['GET', 'POST'])
def handle_bookings():
    if request.method == 'GET':
        return get_bookings()
    elif request.method == 'POST':
        return add_booking()

def get_bookings():
    """Получение списка бронирований"""
    try:
        bookings = Booking.query.all()
        return jsonify([{
            'id': b.id,
            'guest_name': b.guest_name,
            'check_in_date': b.check_in_date.isoformat(),
            'check_out_date': b.check_out_date.isoformat(),
            'room_id': b.room_id,
            'room_number': b.room.number if b.room else None
        } for b in bookings])
    except Exception as e:
        logger.error(f"Error retrieving bookings: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def add_booking():
    """Добавление нового бронирования"""
    try:
        data = request.json

        if not InputValidator.is_safe_input(data):
            return jsonify({"error": "Invalid input data"}), 400

        required_fields = {'guest_name', 'check_in_date', 'check_out_date', 'room_id'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Проверка доступности комнаты
        room = Room.query.get(data['room_id'])
        if not room or not room.available:
            return jsonify({"error": "Room not available"}), 400

        # Проверка пересечения дат
        existing_booking = Booking.query.filter(
            Booking.room_id == data['room_id'],
            Booking.check_in_date <= datetime.strptime(data['check_out_date'], '%Y-%m-%d').date(),
            Booking.check_out_date >= datetime.strptime(data['check_in_date'], '%Y-%m-%d').date()
        ).first()

        if existing_booking:
            return jsonify({"error": "Room already booked for these dates"}), 400

        new_booking = Booking(
            guest_name=data['guest_name'],
            check_in_date=datetime.strptime(data['check_in_date'], '%Y-%m-%d').date(),
            check_out_date=datetime.strptime(data['check_out_date'], '%Y-%m-%d').date(),
            room_id=data['room_id']
        )

        db.session.add(new_booking)
        db.session.commit()

        return jsonify({
            'id': new_booking.id,
            'guest_name': new_booking.guest_name,
            'check_in_date': new_booking.check_in_date.isoformat(),
            'check_out_date': new_booking.check_out_date.isoformat(),
            'room_id': new_booking.room_id
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding booking: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Регистрация обработчиков ошибок
register_error_handlers(app)

# Создание таблиц при запуске
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)