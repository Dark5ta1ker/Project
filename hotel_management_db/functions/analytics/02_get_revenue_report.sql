-- 7. АНАЛИТИЧЕСКИЕ ЗАПРОСЫ

-- 2. Функция 'get_revenue_report'
-- Генерирует отчет о доходах по месяцам, включая сравнение с предыдущим годом.
CREATE OR REPLACE FUNCTION get_revenue_report() 
RETURNS TABLE (
    year 					INTEGER, 		-- Год.
    month 					INTEGER, 		-- Номер месяца.
    month_name 				TEXT, 			-- Название месяца.
    room_revenue 			DECIMAL(12, 2), -- Доход от проживания в номерах.
    service_revenue 		DECIMAL(12, 2), -- Доход от дополнительных услуг.
    total_revenue 			DECIMAL(12, 2), -- Общий доход за месяц.
    prev_year_total_revenue DECIMAL(12, 2), -- Общий доход за тот же месяц предыдущего года.
    revenue_growth 			DECIMAL(10, 2) 	-- Процентный рост дохода по сравнению с предыдущим годом.
) AS $$
BEGIN
    RETURN QUERY
    WITH monthly_data AS ( -- Временная таблица для агрегации месячных данных о доходах.
        SELECT
            EXTRACT(YEAR FROM p.transaction_date)::INTEGER AS year, -- Извлекаем год из даты транзакции.
            EXTRACT(MONTH FROM p.transaction_date)::INTEGER AS month, -- Извлекаем номер месяца.
            TO_CHAR(p.transaction_date, 'Month') AS month_name, -- Преобразуем дату в название месяца.
            SUM(
                CASE
                    WHEN p.amount <= r.daily_rate * (b.check_out_date - b.check_in_date) THEN p.amount -- Если сумма платежа меньше или равна стоимости номера, то вся сумма идет в доход от номера.
                    ELSE r.daily_rate * (b.check_out_date - b.check_in_date) -- Иначе, только стоимость номера.
                END
            ) AS room_revenue, -- Суммарный доход от номеров.
            SUM(
                CASE
                    WHEN p.amount > r.daily_rate * (b.check_out_date - b.check_in_date) THEN p.amount - (r.daily_rate * (b.check_out_date - b.check_in_date)) -- Если сумма платежа превышает стоимость номера, то разница идет в доход от услуг.
                    ELSE 0 -- Иначе, доход от услуг равен 0.
                END
            ) AS service_revenue, -- Суммарный доход от услуг.
            SUM(p.amount) AS total_revenue -- Общий доход (сумма всех платежей).
        FROM
            payments p
            JOIN bookings b ON p.booking_id = b.booking_id -- Соединяем платежи с бронированиями.
            JOIN rooms r ON b.room_id = r.room_id -- Соединяем с номерами для получения ежедневной ставки.
        WHERE
            p.status = 'completed' -- Учитываем только завершенные платежи.
        GROUP BY
            EXTRACT(YEAR FROM p.transaction_date), -- Группируем по году.
            EXTRACT(MONTH FROM p.transaction_date), -- Группируем по месяцу.
            TO_CHAR(p.transaction_date, 'Month') -- Группируем по названию месяца.
    )
    SELECT
        m.year,
        m.month,
        TRIM(m.month_name) AS month_name, -- Удаляем пробелы из названия месяца.
        m.room_revenue,
        m.service_revenue,
        m.total_revenue,
        prev.total_revenue AS prev_year_total_revenue, -- Доход за тот же месяц предыдущего года.
        CASE 
            WHEN prev.total_revenue IS NULL OR prev.total_revenue = 0 THEN NULL -- Если данных за предыдущий год нет или доход был 0, рост не рассчитывается.
            ELSE (m.total_revenue - prev.total_revenue) * 100.0 / prev.total_revenue -- Формула расчета процентного роста.
        END::DECIMAL(10, 2) AS revenue_growth -- Приводим результат к DECIMAL с 2 знаками после запятой.
    FROM
        monthly_data m
        LEFT JOIN monthly_data prev ON m.month = prev.month AND m.year = prev.year + 1 -- Левое самосоединение для получения данных за предыдущий год (месяц совпадает, год на 1 меньше).
    ORDER BY
        m.year, m.month; -- Сортировка по году и месяцу.
END;
$$ LANGUAGE plpgsql;
