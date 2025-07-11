-- Главный скрипт для полного развертывания базы данных системы управления отелем.
-- Запускает все остальные скрипты в правильном порядке.

-- Убедитесь, что вы подключены к нужной базе данных PostgreSQL.

-- 1. Создание схемы и установка пути поиска
\i schema/01_schema_and_search_path.sql

-- 2. Создание пользовательских типов данных
\i schema/02_types.sql

-- 3. Создание таблиц
\i schema/03_tables.sql

-- 4. Создание индексов для производительности
\i indexes/01_create_indexes.sql

-- 5. Создание функций для триггеров
\i triggers/01_update_timestamp_function.sql

-- 6. Создание триггеров
\i triggers/02_create_triggers.sql

-- 7. Вставка демонстрационных данных
\i data/01_insert_guests.sql
\i data/02_insert_rooms.sql
\i data/03_insert_bookings.sql
\i data/04_insert_services.sql
\i data/05_insert_booking_services.sql
\i data/06_insert_payments.sql

-- 8. Создание базовых CRUD функций
\i functions/crud/01_guest_crud.sql
\i functions/crud/02_room_crud.sql
\i functions/crud/03_booking_crud.sql

-- 9. Создание функций бизнес-логики
\i functions/business_logic/01_find_available_rooms.sql
\i functions/business_logic/02_calculate_booking_cost.sql

-- 10. Создание аналитических функций
\i functions/analytics/01_get_occupancy_rate.sql
\i functions/analytics/02_get_revenue_report.sql
\i functions/analytics/03_get_guest_segmentation.sql

-- Развертывание завершено!
SELECT 'База данных отеля успешно развернута!' AS status;
