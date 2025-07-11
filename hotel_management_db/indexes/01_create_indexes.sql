-- 2. ИНДЕКСЫ ДЛЯ ПРОИЗВОДИТЕЛЬНОСТИ
-- Индексы создаются для ускорения операций поиска и фильтрации данных.

CREATE INDEX idx_guests_passport ON guests(passport_number); 				-- Индекс для быстрого поиска гостей по номеру паспорта.
CREATE INDEX idx_rooms_status ON rooms(status); 							-- Индекс для быстрого фильтрации номеров по статусу.
CREATE INDEX idx_bookings_dates ON bookings(check_in_date, check_out_date); -- Индекс для эффективного поиска бронирований по диапазону дат.
CREATE INDEX idx_bookings_guest ON bookings(guest_id); 						-- Индекс для быстрого поиска бронирований по гостю.
CREATE INDEX idx_bookings_room ON bookings(room_id); 						-- Индекс для быстрого поиска бронирований по номеру.
CREATE INDEX idx_payments_booking ON payments(booking_id); 					-- Индекс для быстрого поиска платежей по бронированию.
