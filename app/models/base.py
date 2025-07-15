from sqlalchemy.dialects.postgresql import ENUM  # Для создания пользовательских типов ENUM в PostgreSQL

# Создаем пользовательские типы ENUM для PostgreSQL
# Эти типы используются для ограничения значений полей в таблицах базы данных
room_type = ENUM('Basic', 'Advanced', 'Business', 'Dorm', name='room_type', create_type=True)
room_status = ENUM('available', 'occupied', 'maintenance', 'cleaning', name='room_status', create_type=True)
booking_status = ENUM('confirmed', 'checked_in', 'checked_out', 'cancelled', name='booking_status', create_type=True)
payment_method = ENUM('cash', 'credit_card', 'bank_transfer', 'online', name='payment_method', create_type=True)
payment_status = ENUM('pending', 'completed', 'failed', 'refunded', name='payment_status', create_type=True)
