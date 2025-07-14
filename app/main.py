from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from datetime import datetime
from app.logger_config import setup_logger
from app.error_handlers import register_error_handlers
from app.input_validator import InputValidator
from app.models import db, Guest, Room, CleaningSchedule, Booking, Service, BookingService, Payment

# Загрузка переменных окружения из файла .env
load_dotenv()

# Настройка логгера для записи логов приложения
logger = setup_logger()

# Создание экземпляра приложения Flask
app = Flask(__name__)

# Конфигурация базы данных: подключение к PostgreSQL с использованием переменных окружения
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение отслеживания изменений для оптимизации

# Инициализация базы данных SQLAlchemy в приложении
db.init_app(app)

# Маршруты для работы с гостями
@app.route('/api/guests', methods=['GET', 'POST'])
def handle_guests():
    """
    Обработчик маршрута для получения списка гостей (GET) или добавления нового гостя (POST).
    """
    if request.method == 'GET':
        return get_guests()
    elif request.method == 'POST':
        return add_guest()

def get_guests():
    """
    Получение списка всех гостей из базы данных.
    Возвращает JSON-массив объектов с информацией о каждом госте.
    Если возникает ошибка, возвращает сообщение об ошибке с кодом 500.
    """
    try:
        guests = Guest.query.all()  # Запрос всех записей из таблицы Guest
        return jsonify([guest.to_dict() for guest in guests])  # Преобразование в словарь и возврат JSON
    except Exception as e:
        logger.error(f"Error retrieving guests: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def add_guest():
    """
    Добавление нового гостя в базу данных.
    Проверяет входные данные на наличие обязательных полей и безопасность.
    Возвращает созданный объект гостя в формате JSON с кодом 201.
    При ошибке возвращает сообщение об ошибке с соответствующим кодом.
    """
    try:
        data = request.json  # Получение данных из тела запроса
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
        db.session.add(new_guest)  # Добавление нового гостя в сессию
        db.session.commit()  # Фиксация изменений в базе данных
        return jsonify(new_guest.to_dict()), 201
    except Exception as e:
        db.session.rollback()  # Откат изменений в случае ошибки
        logger.error(f"Error adding guest: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/rooms/<room_number>/full-info', methods=['GET'])
def get_full_room_info(room_number):
    """
    Получение полной информации о номере, включая бронирования, уборку, услуги и оплату.
    Принимает room_number как параметр маршрута.
    Возвращает JSON-объект с детальной информацией о номере.
    """
    try:
        room = Room.query.filter_by(room_number=room_number).first()  # Поиск номера по room_number
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
            "cleaning": [],
            "payments": [],
            "services": []
        }
        bookings = Booking.query.filter_by(room_id=room.room_id).all()  # Получение всех бронирований для номера
        for booking in bookings:
            guest = db.session.get(Guest, booking.guest_id)
            result["bookings"].append({
                "guest_name": f"{guest.first_name} {guest.last_name}",
                "check_in": booking.check_in_date.strftime('%d.%m.%Y'),
                "check_out": booking.check_out_date.strftime('%d.%m.%Y'),
                "status": booking.status
            })
            # Услуги по бронированию
            booking_services = BookingService.query.filter_by(booking_id=booking.booking_id).all()
            for bs in booking_services:
                service = db.session.get(Service, bs.service_id)
                result["services"].append({
                    "service_name": service.name,
                    "quantity": bs.quantity,
                    "date": bs.service_date.strftime('%d.%m.%Y'),
                    "notes": bs.notes or ""
                })
            # Платежи по бронированию
            payments = Payment.query.filter_by(booking_id=booking.booking_id).all()
            for payment in payments:
                result["payments"].append({
                    "amount": float(payment.amount),
                    "status": payment.status,
                    "method": payment.method,
                    "date": payment.transaction_date.strftime('%d.%m.%Y') if payment.transaction_date else "—"
                })
        # Уборка
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

@app.route('/ui/services-by-date', methods=['GET'])
def get_services_by_date():
    """
    Получение списка услуг за указанный период.
    Принимает параметры start_date и end_date в формате YYYY-MM-DD.
    Возвращает JSON-массив объектов с информацией об услугах.
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        if not start_date_str or not end_date_str:
            return jsonify({"error": "Missing date range"}), 400
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        if end_date < start_date:
            return jsonify({"error": "Invalid date range"}), 400
        booking_services = (
            db.session.query(BookingService, Booking, Room, Service)
            .join(Booking, Booking.booking_id == BookingService.booking_id)
            .join(Room, Room.room_id == Booking.room_id)
            .join(Service, Service.service_id == BookingService.service_id)
            .filter(BookingService.service_date >= start_date)
            .filter(BookingService.service_date <= end_date)
            .order_by(BookingService.service_date)
            .all()
        )
        results = []
        for bs, booking, room, service in booking_services:
            results.append({
                "date": bs.service_date.strftime('%d.%m.%Y'),
                "room_number": room.room_number,
                "service_name": service.name,
                "quantity": bs.quantity,
                "notes": bs.notes or ""
            })
        return jsonify(results)
    except Exception as e:
        logger.error(f"Ошибка при получении услуг за период: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

# Маршруты для работы с комнатами
@app.route('/api/rooms', methods=['GET', 'POST'])
def handle_rooms():
    """
    Обработчик маршрута для получения списка комнат (GET) или добавления новой комнаты (POST).
    """
    if request.method == 'GET':
        return get_rooms()
    elif request.method == 'POST':
        return add_room()

def get_rooms():
    """
    Получение списка комнат с возможностью фильтрации по статусу, вместимости и датам.
    Возвращает JSON-массив объектов с информацией о комнатах.
    """
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
    """
    Добавление новой комнаты в базу данных.
    Проверяет входные данные на наличие обязательных полей и безопасность.
    Возвращает созданный объект комнаты в формате JSON с кодом 201.
    """
    try:
        data = request.json
        if not InputValidator.is_safe_input(data):
            return jsonify({"error": "Invalid input data"}), 400
        required_fields = {'room_number', 'type', 'capacity', 'daily_rate'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
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
    """
    Обработчик маршрута для получения расписания уборки (GET),
    добавления новой записи (POST) или обновления существующей (PUT).
    """
    if request.method == 'GET':
        return get_cleaning_schedule()
    elif request.method == 'POST':
        return add_cleaning_schedule()
    elif request.method == 'PUT':
        return update_cleaning_schedule()

def get_cleaning_schedule():
    """
    Получение расписания уборки для всех комнат.
    Возвращает JSON-массив объектов с информацией о расписании.
    """
    try:
        schedules = CleaningSchedule.query.all()
        return jsonify([schedule.to_dict() for schedule in schedules])
    except Exception as e:
        logger.error(f"Error retrieving cleaning schedule: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def add_cleaning_schedule():
    """
    Добавление новой записи в расписание уборки.
    Проверяет входные данные на наличие обязательных полей и безопасность.
    Возвращает созданный объект расписания в формате JSON с кодом 201.
    """
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
    """
    Обновление записи в расписании уборки.
    Проверяет входные данные на наличие обязательных полей и безопасность.
    Возвращает обновленный объект расписания в формате JSON.
    """
    try:
        data = request.json
        if not InputValidator.is_safe_input(data):
            return jsonify({"error": "Invalid input data"}), 400
        required_fields = {'id', 'needs_cleaning'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        schedule = db.session.get(CleaningSchedule, data['id'])
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
    """
    Обработчик маршрута для получения списка бронирований (GET)
    или добавления нового бронирования (POST).
    """
    if request.method == 'GET':
        return get_bookings()
    elif request.method == 'POST':
        return add_booking()

def get_bookings():
    """
    Получение списка всех бронирований.
    Возвращает JSON-массив объектов с информацией о бронированиях.
    """
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

        # 1. Проверка обязательных полей
        required_fields = {'room_id', 'check_in_date', 'check_out_date', 'adults', 'guest'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # 2. Получение и валидация гостя
        guest_data = data['guest']
        if 'passport_number' not in guest_data:
            return jsonify({"error": "Passport number required"}), 400

        passport_number = guest_data['passport_number'].upper()

        guest = Guest.query.filter_by(passport_number=passport_number).first()
        if not guest:
            guest = Guest(
                passport_number=passport_number,
                first_name=guest_data['first_name'],
                last_name=guest_data['last_name'],
                phone=guest_data['phone'],
                email=guest_data.get('email'),
                address=guest_data.get('address')
            )
            db.session.add(guest)
            db.session.flush()  # чтобы получить guest.guest_id до commit

        # 3. Проверка номера
        room = db.session.get(Room, data['room_id'])
        if not room or room.status != 'available':
            return jsonify({"error": "Room not available"}), 400

        # 4. Проверка вместимости
        if data['adults'] + data.get('children', 0) > room.capacity:
            return jsonify({"error": "Room capacity exceeded"}), 400

        # 5. Проверка пересечений
        existing_booking = Booking.query.filter(
            Booking.room_id == data['room_id'],
            Booking.check_in_date <= datetime.strptime(data['check_out_date'], '%Y-%m-%d').date(),
            Booking.check_out_date >= datetime.strptime(data['check_in_date'], '%Y-%m-%d').date(),
            Booking.status != 'cancelled'
        ).first()

        if existing_booking:
            return jsonify({"error": "Room already booked for these dates"}), 400

        # 6. Создание брони
        new_booking = Booking(
            guest_id=guest.guest_id,
            room_id=data['room_id'],
            check_in_date=datetime.strptime(data['check_in_date'], '%Y-%m-%d').date(),
            check_out_date=datetime.strptime(data['check_out_date'], '%Y-%m-%d').date(),
            adults=data['adults'],
            children=data.get('children', 0),
            status='confirmed'
        )

        db.session.add(new_booking)
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
    """
    Обработчик маршрута для получения списка услуг (GET)
    или добавления новой услуги (POST).
    """
    if request.method == 'GET':
        return get_services()
    elif request.method == 'POST':
        return add_service()

def get_services():
    """
    Получение списка активных услуг.
    Возвращает JSON-массив объектов с информацией об услугах.
    """
    try:
        services = Service.query.filter_by(is_active=True).all()
        return jsonify([service.to_dict() for service in services])
    except Exception as e:
        logger.error(f"Error retrieving services: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def add_service():
    """
    Добавление новой услуги в базу данных.
    Проверяет входные данные на наличие обязательных полей и безопасность.
    Возвращает созданный объект услуги в формате JSON с кодом 201.
    """
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
    """
    Обработчик маршрута для получения списка платежей (GET)
    или добавления нового платежа (POST).
    """
    if request.method == 'GET':
        return get_payments()
    elif request.method == 'POST':
        return add_payment()

def get_payments():
    """
    Получение списка всех платежей.
    Возвращает JSON-массив объектов с информацией о платежах.
    """
    try:
        payments = Payment.query.all()
        return jsonify([payment.to_dict() for payment in payments])
    except Exception as e:
        logger.error(f"Error retrieving payments: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

def add_payment():
    """
    Добавление нового платежа в базу данных.
    Проверяет входные данные на наличие обязательных полей и безопасность.
    Возвращает созданный объект платежа в формате JSON с кодом 201.
    """
    try:
        data = request.json
        if not InputValidator.is_safe_input(data):
            return jsonify({"error": "Invalid input data"}), 400
        required_fields = {'booking_id', 'amount', 'method'}
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        booking = db.session.get(Booking, data['booking_id'])
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
    """
    Контроллер для фронта: отдает отфильтрованный список комнат.
    Использует ту же логику, что и get_rooms.
    """
    try:
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