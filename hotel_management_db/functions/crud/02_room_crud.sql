-- 5. БАЗОВЫЕ CRUD ФУНКЦИИ

-- CRUD операции для номеров

-- Функция 'create_room'
-- Создает новую запись о номере в таблице 'rooms'.
-- Возвращает 'room_id' вновь созданной записи.
CREATE OR REPLACE FUNCTION create_room(
    p_room_number 		VARCHAR(10), 		-- Номер комнаты.
    p_type 				room_type, 			-- Тип номера.
    p_capacity 			SMALLINT, 			-- Вместимость.
    p_daily_rate 		DECIMAL(10, 2), 	-- Ежедневная ставка.
    p_description 		TEXT DEFAULT NULL 	-- Описание номера (необязательно).
) RETURNS INTEGER AS $$
DECLARE
    new_id INTEGER;
BEGIN
    INSERT INTO rooms (room_number, type, capacity, daily_rate, description)
    VALUES (p_room_number, p_type, p_capacity, p_daily_rate, p_description)
    RETURNING room_id INTO new_id; -- Вставляет данные и возвращает сгенерированный room_id.
    
    RETURN new_id; -- Возвращает ID нового номера.
END;
$$ LANGUAGE plpgsql;

-- Функция 'update_room_status'
-- Обновляет статус номера.
CREATE OR REPLACE FUNCTION update_room_status(
    p_room_id 			INTEGER, 	-- Идентификатор номера.
    p_status 			room_status -- Новый статус номера.
) RETURNS VOID AS $$
BEGIN
    UPDATE rooms SET status = p_status WHERE room_id = p_room_id; -- Обновляет статус номера по room_id.
END;
$$ LANGUAGE plpgsql;
