-- 6. ФУНКЦИИ БИЗНЕС-ЛОГИКИ
-- Более сложные функции, реализующие бизнес-правила отеля.

-- Функция 'find_available_rooms'
-- Находит доступные номера для бронирования в заданном диапазоне дат,
-- с возможностью фильтрации по типу и минимальной вместимости.
CREATE OR REPLACE FUNCTION find_available_rooms(
    p_check_in 			DATE, 					-- Желаемая дата заезда.
    p_check_out 		DATE, 					-- Желаемая дата выезда.
    p_room_type 		room_type DEFAULT NULL, -- Желаемый тип номера (необязательно).
    p_capacity 			SMALLINT DEFAULT NULL 	-- Минимальная желаемая вместимость (необязательно).
) RETURNS TABLE (
    room_id 			INTEGER,
    room_number 		VARCHAR(10),
    type 				room_type,
    capacity 			SMALLINT,
    daily_rate 			DECIMAL(10, 2),
    description 		TEXT,
    total_cost 			DECIMAL(10, 2) 			-- Общая стоимость проживания за указанный период.
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.room_id,
        r.room_number,
        r.type,
        r.capacity,
        r.daily_rate,
        r.description,
        r.daily_rate * (p_check_out - p_check_in) AS total_cost -- Расчет общей стоимости: ежедневная ставка * количество ночей.
    FROM 
        rooms r
    WHERE 
        r.status = 'available' -- Ищем только номера со статусом 'available'.
        AND (p_room_type IS NULL OR r.type = p_room_type) -- Фильтр по типу номера, если указан.
        AND (p_capacity IS NULL OR r.capacity >= p_capacity) -- Фильтр по вместимости, если указана.
        AND NOT EXISTS ( -- Исключаем номера, которые уже забронированы (или имеют пересекающиеся бронирования) в заданный период.
            SELECT 1 FROM bookings b
            WHERE b.room_id = r.room_id
            AND b.status <> 'cancelled' -- Исключаем отмененные бронирования.
            AND b.check_in_date < p_check_out -- Проверка на пересечение дат: заезд текущего бронирования до выезда искомого периода.
            AND b.check_out_date > p_check_in -- И выезд текущего бронирования после заезда искомого периода.
        )
    ORDER BY r.daily_rate; -- Сортировка по ежедневной ставке.
END;
$$ LANGUAGE plpgsql;
