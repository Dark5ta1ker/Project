-- 5. БАЗОВЫЕ CRUD ФУНКЦИИ

-- CRUD операции для бронирований

-- Функция 'create_booking'
-- Создает новое бронирование.
-- Автоматически изменяет статус забронированного номера на 'reserved'.
-- Возвращает 'booking_id' вновь созданной записи.
CREATE OR REPLACE FUNCTION create_booking(
    p_guest_id 			INTEGER, 			-- Идентификатор гостя.
    p_room_id 			INTEGER, 			-- Идентификатор номера.
    p_check_in 			DATE, 				-- Дата заезда.
    p_check_out 		DATE, 				-- Дата выезда.
    p_adults 			SMALLINT DEFAULT 1, -- Количество взрослых.
    p_children 			SMALLINT DEFAULT 0 	-- Количество детей.
) RETURNS INTEGER AS $$
DECLARE
    new_id 				INTEGER;
BEGIN
    INSERT INTO bookings (guest_id, room_id, check_in_date, check_out_date, adults, children)
    VALUES (p_guest_id, p_room_id, p_check_in, p_check_out, p_adults, p_children)
    RETURNING booking_id INTO new_id; -- Вставляет данные и возвращает сгенерированный booking_id.
    
    -- Вызывает функцию для изменения статуса номера на 'reserved' (зарезервирован).
    PERFORM update_room_status(p_room_id, 'reserved'); 
    
    RETURN new_id; -- Возвращает ID нового бронирования.
END;
$$ LANGUAGE plpgsql;

-- Функция 'update_booking_status'
-- Обновляет статус бронирования и соответствующий статус номера.
CREATE OR REPLACE FUNCTION update_booking_status(
    p_booking_id 		INTEGER, 		-- Идентификатор бронирования.
    p_status 			booking_status 	-- Новый статус бронирования.
) RETURNS VOID AS $$
DECLARE
    v_room_id 			INTEGER; 		-- Переменная для хранения ID номера, связанного с бронированием.
BEGIN
    -- Получаем room_id из бронирования.
    SELECT room_id INTO v_room_id FROM bookings WHERE booking_id = p_booking_id;
    
    -- Обновляем статус бронирования.
    UPDATE bookings SET status = p_status WHERE booking_id = p_booking_id;
    
    -- Обновляем статус номера на основе нового статуса бронирования.
    IF p_status = 'checked_in' THEN -- Если статус 'checked_in' (заселен), номер становится 'occupied' (занят).
        PERFORM update_room_status(v_room_id, 'occupied');
    ELSIF p_status = 'checked_out' OR p_status = 'cancelled' THEN -- Если статус 'checked_out' (выписан) или 'cancelled' (отменен), номер становится 'available' (доступен).
        PERFORM update_room_status(v_room_id, 'available');
    END IF;
END;
$$ LANGUAGE plpgsql;
