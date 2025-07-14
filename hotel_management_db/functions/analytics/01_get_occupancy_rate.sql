-- 7. АНАЛИТИЧЕСКИЕ ЗАПРОСЫ
-- Функции для получения агрегированных данных и отчетов.

-- 1. Функция 'get_occupancy_rate'
-- Рассчитывает коэффициент загрузки номеров по типам за определенный период.
-- Коэффициент загрузки = (количество занятых ночей / общее количество доступных ночей) * 100%.
CREATE OR REPLACE FUNCTION get_occupancy_rate(
    p_start_date 		DATE, 			-- Начальная дата периода.
    p_end_date 			DATE 			-- Конечная дата периода.
) RETURNS TABLE (
    room_type 			room_type, 		-- Тип номера.
    total_rooms 		INTEGER, 		-- Общее количество номеров данного типа.
    booked_rooms 		INTEGER, 		-- Количество уникальных номеров данного типа, которые были забронированы в период.
    occupancy_rate 		DECIMAL(5, 2) 	-- Коэффициент загрузки в процентах.
) AS $$
BEGIN
    RETURN QUERY
    WITH room_type_stats AS ( -- Временная таблица (CTE) для предварительного расчета статистики по типам номеров.
        SELECT 
            r.type,
            COUNT(r.room_id) AS total_rooms_of_type, -- Общее количество номеров данного типа.
            SUM(
                CASE 
                    WHEN b.booking_id IS NOT NULL -- Если есть бронирование, которое пересекается с периодом.
                         AND b.status <> 'cancelled' -- И бронирование не отменено.
                         AND b.check_in_date < p_end_date 
                         AND b.check_out_date > p_start_date
                    THEN LEAST(b.check_out_date, p_end_date) - GREATEST(b.check_in_date, p_start_date) -- Вычисляет количество ночей пересечения.
                    ELSE 0 -- Если нет пересечений или бронирование отменено, то 0 ночей.
                END
            ) AS occupied_room_days_in_period, -- Сумма занятых ночей для данного типа номера в периоде.
            COUNT(DISTINCT b.room_id) FILTER ( -- Подсчет уникальных номеров, которые были забронированы в период.
                WHERE b.booking_id IS NOT NULL 
                  AND b.status <> 'cancelled' 
                  AND b.check_in_date < p_end_date 
                  AND b.check_out_date > p_start_date
            ) AS unique_booked_rooms_in_period
        FROM 
            rooms r
            LEFT JOIN bookings b ON r.room_id = b.room_id -- Левое соединение, чтобы включить номера без бронирований.
        GROUP BY r.type -- Группировка по типу номера.
    )
    SELECT 
        rts.type,
        rts.total_rooms_of_type,
        rts.unique_booked_rooms_in_period,
        COALESCE( -- Используем COALESCE, чтобы избежать деления на ноль, если нет доступных ночей.
            (rts.occupied_room_days_in_period * 100.0) / -- Занятые ночи * 100
            (rts.total_rooms_of_type * (p_end_date - p_start_date)), -- Делим на общее количество доступных ночей (количество номеров * дней в периоде).
            0.00
        )::DECIMAL(5, 2) AS occupancy_rate -- Приводим результат к DECIMAL с 2 знаками после запятой.
    FROM 
        room_type_stats rts
    ORDER BY rts.type; -- Сортировка по типу номера.
END;
$$ LANGUAGE plpgsql;
