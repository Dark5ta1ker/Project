-- Пользовательский тип 'room_type' (Тип номера)
-- Определяет допустимые категории номеров.
CREATE TYPE room_type AS ENUM ('single', 'double', 'suite', 'dormitory');

-- Пользовательский тип 'room_status' (Статус номера)
-- Определяет текущее состояние номера.
CREATE TYPE room_status AS ENUM ('available', 'occupied', 'maintenance', 'reserved');

-- Пользовательский тип 'booking_status' (Статус бронирования)
-- Определяет этапы жизненного цикла бронирования.
CREATE TYPE booking_status AS ENUM ('confirmed', 'checked_in', 'checked_out', 'cancelled');

-- Пользовательский тип 'payment_method' (Метод оплаты)
-- Определяет допустимые способы оплаты.
CREATE TYPE payment_method AS ENUM ('cash', 'credit_card', 'bank_transfer', 'online');

-- Пользовательский тип 'payment_status' (Статус платежа)
-- Определяет текущее состояние платежа.
CREATE TYPE payment_status AS ENUM ('pending', 'completed', 'failed', 'refunded');
