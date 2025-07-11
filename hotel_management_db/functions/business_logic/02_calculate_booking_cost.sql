-- 6. ФУНКЦИИ БИЗНЕС-ЛОГИКИ

-- Функция 'calculate_booking_cost'
-- Рассчитывает полную стоимость бронирования, включая стоимость номера и использованные услуги.
CREATE OR REPLACE FUNCTION calculate_booking_cost(p_booking_id INTEGER) 
RETURNS DECIMAL(10, 2) AS $$
DECLARE
    v_room_cost 		DECIMAL(10, 2); -- Переменная для хранения стоимости номера.
    v_services_cost 	DECIMAL(10, 2); -- Переменная для хранения стоимости услуг.
BEGIN
    -- Рассчитываем стоимость номера для данного бронирования.
    SELECT 
        r.daily_rate * (b.check_out_date - b.check_in_date) -- Стоимость = ставка * количество ночей.
    INTO 
        v_room_cost
    FROM 
        bookings b
        JOIN rooms r ON b.room_id = r.room_id
    WHERE 
        b.booking_id = p_booking_id;
    
    -- Рассчитываем общую стоимость услуг для данного бронирования.
    SELECT 
        COALESCE(SUM(s.price * bs.quantity), 0) -- Суммируем (цена услуги * количество). COALESCE возвращает 0, если услуг нет (SUM вернет NULL).
    INTO 
        v_services_cost
    FROM 
        booking_services bs
        JOIN services s ON bs.service_id = s.service_id
    WHERE 
        bs.booking_id = p_booking_id;
    
    RETURN v_room_cost + v_services_cost; -- Возвращаем общую стоимость.
END;
$$ LANGUAGE plpgsql;
