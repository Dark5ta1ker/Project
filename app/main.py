from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from datetime import datetime
from app.logger_config import setup_logger
from app.error_handlers import register_error_handlers
from app.input_validator import InputValidator
from app.models import db, Guest, Room, CleaningSchedule, Booking, Service, BookingService, Payment

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

# Маршруты для работы с гостями
@app.route('/api/guests', methods=['GET', 'POST'])
def handle_guests():
    if request.method == 'GET':
        return get_guests()
    elif request.method == 'POST':
        return add_guest()

def get_guests():
    """Получение списка гостей"""
    try:
        guests = Guest.query.all()
        return jsonify([guest.to_dict() for guest in guests])
    except Exception as e:
        logger.error(f"Error retrieving guests: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def add_guest():
    """Добавление нового гостя"""
    try:
        data = request.json

        if not InputValidator.is_safe_input(data):
            return jsonify({"error": "Invalid input data"}), 400

        required_fields = {'passport_number', 'first_name', 'last_name', 'phone'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        new_guest = Guest(
            passport_number=data['passport_number'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            email=data.get('email'),
            address=data.get('address')
        )

        db.session.add(new_guest)
        db.session.commit()

        return jsonify(new_guest.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding guest: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/rooms/<room_number>/full-info', methods=['GET'])
def get_full_room_info(room_number):
    """Возвращает полную информацию о номере в формате для фронтенда"""
    try:
        # 1. Получаем основную информацию о номере
        room = Room.query.filter_by(room_number=room_number).first()
        if not room:
            return jsonify({"error": "Room not found"}), 404
        
        result = {
            "room_info": {
                "room_number": room.room_number,
                "type": room.type,
                "capacity": room.capacity,
                "status": room.status,
                "daily_rate": float(room.daily_rate),
                "description": room.description
            },
            "bookings": [],
            "cleaning": []
        }
        
        # 2. Получаем информацию о бронированиях
        bookings = Booking.query.filter_by(room_id=room.room_id).all()
        for booking in bookings:
            guest = Guest.query.get(booking.guest_id)
            result["bookings"].append({
                "guest_name": f"{guest.first_name} {guest.last_name}",
                "check_in": booking.check_in_date.strftime('%d.%m.%Y'),
                "check_out": booking.check_out_date.strftime('%d.%m.%Y'),
                "status": booking.status
            })
        
        # 3. Получаем информацию об уборке
        cleaning = CleaningSchedule.query.filter_by(room_id=room.room_id).first()
        if cleaning:
            result["cleaning"].append({
                "date": cleaning.next_cleaning_date.strftime('%d.%m.%Y') if cleaning.next_cleaning_date else None,
                "needs_cleaning": cleaning.needs_cleaning
            })
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting full room info: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Маршруты для работы с комнатами
@app.route('/api/rooms', methods=['GET', 'POST'])
def handle_rooms():
    if request.method == 'GET':
        return get_rooms()
    elif request.method == 'POST':
        return add_room()

def get_rooms():
    try:
        status = request.args.get('status')
        capacity = request.args.get('capacity')
        min_capacity = request.args.get('min_capacity')
        check_in = request.args.get('check_in')
        check_out = request.args.get('check_out')

        query = Room.query

        # Фильтр по вместимости
        if capacity and capacity.isdigit():
            query = query.filter(Room.capacity == int(capacity))
        elif min_capacity and min_capacity.isdigit():
            query = query.filter(Room.capacity >= int(min_capacity))

        # Проверка дат
        if check_in and check_out:
            try:
                check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
                check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()

                # Подзапрос: номера, ЗАНЯТЫЕ в заданный период
                booked_room_ids = db.session.query(Booking.room_id).filter(
                    Booking.check_in_date <= check_out_date,
                    Booking.check_out_date >= check_in_date,
                    Booking.status != 'cancelled'
                ).subquery()

                if status == "available":
                    query = query.filter(~Room.room_id.in_(booked_room_ids))
                elif status == "occupied":
                    query = query.filter(Room.room_id.in_(booked_room_ids))
                elif status == "maintenance":
                    query = query.filter(Room.status == 'maintenance')
                # статус "все" или None — ничего не фильтруем

            except ValueError as e:
                logger.warning(f"Invalid date format: {e}")
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        else:
            # если даты не заданы, фильтруем только по room.status
            if status == "available":
                query = query.filter(Room.status == 'available')
            elif status == "occupied":
                query = query.filter(Room.status != 'available')
            elif status == "maintenance":
                query = query.filter(Room.status == 'maintenance')

        rooms = query.all()
        results = []
        for room in rooms:
            room_dict = room.to_dict()

            if check_in and check_out:
                # Вычисляем динамический статус
                overlapping_booking = Booking.query.filter(
                    Booking.room_id == room.room_id,
                    Booking.check_in_date <= check_out_date,
                    Booking.check_out_date >= check_in_date,
                    Booking.status != 'cancelled'
                ).first()

                if overlapping_booking:
                    room_dict['dynamic_status'] = 'occupied'
                else:
                    room_dict['dynamic_status'] = 'available'
            else:
                room_dict['dynamic_status'] = room.status  # если нет дат — обычный статус

            results.append(room_dict)

        return jsonify(results)

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

        required_fields = {'room_number', 'type', 'capacity', 'daily_rate'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Создание новой комнаты
        new_room = Room(
            room_number=data['room_number'],
            type=data['type'],
            capacity=data['capacity'],
            daily_rate=data['daily_rate'],
            status=data.get('status', 'available'),
            description=data.get('description')
        )

        db.session.add(new_room)
        db.session.commit()

        # Создание расписания уборки для новой комнаты
        cleaning_schedule = CleaningSchedule(
            room_id=new_room.room_id,
            needs_cleaning=False,
            next_cleaning_date=None
        )
        db.session.add(cleaning_schedule)
        db.session.commit()

        return jsonify(new_room.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding room: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Маршруты для работы с уборкой
@app.route('/api/cleaning-schedule', methods=['GET', 'POST', 'PUT'])
def handle_cleaning():
    if request.method == 'GET':
        return get_cleaning_schedule()
    elif request.method == 'POST':
        return add_cleaning_schedule()
    elif request.method == 'PUT':
        return update_cleaning_schedule()

def get_cleaning_schedule():
    """Получение расписания уборки"""
    try:
        schedules = CleaningSchedule.query.all()
        return jsonify([schedule.to_dict() for schedule in schedules])
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

        return jsonify(new_schedule.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding cleaning schedule: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def update_cleaning_schedule():
    """Обновление расписания уборки"""
    try:
        data = request.json

        if not InputValidator.is_safe_input(data):
            return jsonify({"error": "Invalid input data"}), 400

        required_fields = {'id', 'needs_cleaning'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        schedule = CleaningSchedule.query.get(data['id'])
        if not schedule:
            return jsonify({"error": "Cleaning schedule not found"}), 404

        schedule.needs_cleaning = data['needs_cleaning']
        if 'next_cleaning_date' in data:
            schedule.next_cleaning_date = datetime.strptime(data['next_cleaning_date'], '%Y-%m-%d').date()

        db.session.commit()
        return jsonify(schedule.to_dict())

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating cleaning schedule: {str(e)}", exc_info=True)
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
        return jsonify([booking.to_dict() for booking in bookings])
    except Exception as e:
        logger.error(f"Error retrieving bookings: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def add_booking():
    """Добавление нового бронирования"""
    try:
        data = request.json

        if not InputValidator.is_safe_input(data):
            return jsonify({"error": "Invalid input data"}), 400

        required_fields = {'guest_id', 'room_id', 'check_in_date', 'check_out_date', 'adults'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Проверка существования гостя
        guest = Guest.query.get(data['guest_id'])
        if not guest:
            return jsonify({"error": "Guest not found"}), 404

        # Проверка доступности комнаты
        room = Room.query.get(data['room_id'])
        if not room or room.status != 'available':
            return jsonify({"error": "Room not available"}), 400

        # Проверка вместимости
        if data['adults'] + data.get('children', 0) > room.capacity:
            return jsonify({"error": "Room capacity exceeded"}), 400

        # Проверка пересечения дат
        existing_booking = Booking.query.filter(
            Booking.room_id == data['room_id'],
            Booking.check_in_date <= datetime.strptime(data['check_out_date'], '%Y-%m-%d').date(),
            Booking.check_out_date >= datetime.strptime(data['check_in_date'], '%Y-%m-%d').date(),
            Booking.status != 'cancelled'
        ).first()

        if existing_booking:
            return jsonify({"error": "Room already booked for these dates"}), 400

        new_booking = Booking(
            guest_id=data['guest_id'],
            room_id=data['room_id'],
            check_in_date=datetime.strptime(data['check_in_date'], '%Y-%m-%d').date(),
            check_out_date=datetime.strptime(data['check_out_date'], '%Y-%m-%d').date(),
            adults=data['adults'],
            children=data.get('children', 0),
            status='confirmed'
        )

        db.session.add(new_booking)
        
        # Обновляем статус комнаты
        room.status = 'occupied'
        
        db.session.commit()

        return jsonify(new_booking.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding booking: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Маршруты для работы с услугами
@app.route('/api/services', methods=['GET', 'POST'])
def handle_services():
    if request.method == 'GET':
        return get_services()
    elif request.method == 'POST':
        return add_service()

def get_services():
    """Получение списка услуг"""
    try:
        services = Service.query.filter_by(is_active=True).all()
        return jsonify([service.to_dict() for service in services])
    except Exception as e:
        logger.error(f"Error retrieving services: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def add_service():
    """Добавление новой услуги"""
    try:
        data = request.json

        if not InputValidator.is_safe_input(data):
            return jsonify({"error": "Invalid input data"}), 400

        required_fields = {'name', 'price'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        new_service = Service(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            is_active=data.get('is_active', True)
        )

        db.session.add(new_service)
        db.session.commit()

        return jsonify(new_service.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding service: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Маршруты для работы с платежами
@app.route('/api/payments', methods=['GET', 'POST'])
def handle_payments():
    if request.method == 'GET':
        return get_payments()
    elif request.method == 'POST':
        return add_payment()

def get_payments():
    """Получение списка платежей"""
    try:
        payments = Payment.query.all()
        return jsonify([payment.to_dict() for payment in payments])
    except Exception as e:
        logger.error(f"Error retrieving payments: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def add_payment():
    """Добавление нового платежа"""
    try:
        data = request.json

        if not InputValidator.is_safe_input(data):
            return jsonify({"error": "Invalid input data"}), 400

        required_fields = {'booking_id', 'amount', 'method'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Проверка существования бронирования
        booking = Booking.query.get(data['booking_id'])
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        new_payment = Payment(
            booking_id=data['booking_id'],
            amount=data['amount'],
            method=data['method'],
            status=data.get('status', 'pending'),
            notes=data.get('notes')
        )

        db.session.add(new_payment)
        db.session.commit()

        return jsonify(new_payment.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding payment: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# UI-маршрут для фронта (Qt) — список комнат
@app.route('/ui/rooms', methods=['GET'])
def ui_get_rooms():
    """Контроллер для фронта: отдает отфильтрованный список комнат"""
    try:
        # Используем ту же логику, что и в get_rooms
        return get_rooms()
    except Exception as e:
        logger.error(f"UI: Ошибка получения списка комнат: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Регистрация обработчиков ошибок
register_error_handlers(app)

# Создание таблиц при запуске
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)