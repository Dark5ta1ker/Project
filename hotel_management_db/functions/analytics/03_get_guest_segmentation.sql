-- 7. АНАЛИТИЧЕСКИЕ ЗАПРОСЫ

-- 3. Функция 'get_guest_segmentation'
-- Сегментирует гостей на основе их активности:
-- - Общее количество бронирований
-- - Общее количество ночей проживания
-- - Общие расходы
-- - Дата последнего визита
CREATE OR REPLACE FUNCTION get_guest_segmentation() 
RETURNS TABLE (
    guest_id 				INTEGER, 		-- Идентификатор гостя.
    full_name 				TEXT, 			-- Полное имя гостя.
    total_bookings 			INTEGER, 		-- Общее количество бронирований гостя.
    total_nights 			INTEGER, 		-- Общее количество ночей, проведенных гостем.
    total_spending 			DECIMAL(12, 2), -- Общая сумма, потраченная гостем.
    avg_spending_per_night 	DECIMAL(10, 2), -- Средние расходы за ночь.
    last_visit 				DATE, 			-- Дата последнего выезда гостя.
    segment 				TEXT 			-- Сегмент, к которому относится гость (VIP, Loyal, New, Dormant, Regular, No Bookings).
) AS $$
BEGIN
    RETURN QUERY
    WITH guest_stats AS ( -- Временная таблица для сбора основных статистических данных по каждому гостю.
        SELECT
            g.guest_id,
            g.first_name || ' ' || g.last_name AS full_name, -- Объединяем имя и фамилию.
            COUNT(DISTINCT b.booking_id) AS total_bookings, -- Подсчет уникальных бронирований.
            SUM(b.check_out_date - b.check_in_date) AS total_nights, -- Суммирование количества ночей по всем бронированиям.
            COALESCE(SUM(p.amount), 0) AS total_spending, -- Суммирование всех завершенных платежей. COALESCE для 0, если платежей нет.
            MAX(b.check_out_date) AS last_visit -- Последняя дата выезда.
        FROM
            guests g
            LEFT JOIN bookings b ON g.guest_id = b.guest_id -- Левое соединение, чтобы включить гостей, у которых может не быть бронирований.
            LEFT JOIN payments p ON b.booking_id = p.booking_id AND p.status = 'completed' -- Соединяем с платежами, учитывая только завершенные.
        WHERE
            b.status = 'checked_out' OR b.status IS NULL -- Учитываем только завершенные бронирования для статистики, но включаем всех гостей.
        GROUP BY
            g.guest_id, g.first_name, g.last_name -- Группируем по гостю.
    )
    SELECT
        gs.guest_id,
        gs.full_name,
        gs.total_bookings,
        gs.total_nights,
        gs.total_spending,
        CASE 
            WHEN gs.total_nights IS NULL OR gs.total_nights = 0 THEN 0 -- Избегаем деления на ноль, если ночей нет.
            ELSE gs.total_spending / gs.total_nights -- Расчет средних расходов за ночь.
        END::DECIMAL(10, 2) AS avg_spending_per_night,
        gs.last_visit,
        CASE
            WHEN gs.total_bookings >= 3 AND gs.total_spending >= 30000 THEN 'VIP' -- VIP: 3+ бронирований и расходы 30000+
            WHEN gs.total_bookings >= 2 AND gs.total_spending >= 15000 THEN 'Loyal' -- Лояльный: 2+ бронирований и расходы 15000+
            WHEN gs.total_bookings = 0 THEN 'No Bookings' -- Нет бронирований: гость есть, но не бронировал.
            WHEN gs.last_visit < CURRENT_DATE - INTERVAL '1 year' THEN 'Dormant' -- Неактивный: последний визит более года назад.
            WHEN gs.total_bookings = 1 THEN 'New' -- Новый: только одно бронирование.
            ELSE 'Regular' -- Обычный: все остальные.
        END AS segment -- Определяем сегмент гостя.
    FROM
        guest_stats gs
    ORDER BY
        total_spending DESC; -- Сортировка по убыванию общих расходов.
END;
$$ LANGUAGE plpgsql;
