-- 3. ТРИГГЕРЫ ДЛЯ АВТОМАТИЧЕСКОГО ОБНОВЛЕНИЯ ПОЛЯ UPDATED_AT

-- Триггер 'update_guest_timestamp'
-- Привязывает функцию update_timestamp() к таблице 'guests'.
CREATE TRIGGER update_guest_timestamp
BEFORE UPDATE ON guests -- Срабатывает перед каждой операцией UPDATE на таблице 'guests'.
FOR EACH ROW EXECUTE FUNCTION update_timestamp(); -- Выполняется для каждой изменяемой строки.

-- Добавьте здесь другие триггеры для других таблиц, если они нужны (например, для rooms, bookings, services).
-- Пример для rooms:
-- CREATE TRIGGER update_room_timestamp
-- BEFORE UPDATE ON rooms
-- FOR EACH ROW EXECUTE FUNCTION update_timestamp();
