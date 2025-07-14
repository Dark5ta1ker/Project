-- 5. БАЗОВЫЕ CRUD ФУНКЦИИ
-- Функции для выполнения основных операций: Создание (Create), Чтение (Read - неявно через SELECT), Обновление (Update), Удаление (Delete).

-- CRUD операции для гостей

-- Функция 'create_guest'
-- Создает новую запись о госте в таблице 'guests'.
-- Возвращает 'guest_id' вновь созданной записи.
CREATE OR REPLACE FUNCTION create_guest(
    p_passport 			VARCHAR(20), 				-- Номер паспорта нового гостя.
    p_first_name 		VARCHAR(50), 				-- Имя нового гостя.
    p_last_name 		VARCHAR(50), 				-- Фамилия нового гостя.
    p_phone 			VARCHAR(20), 				-- Телефон нового гостя.
    p_email 			VARCHAR(100) DEFAULT NULL, 	-- Email нового гостя (необязательно).
    p_address 			TEXT DEFAULT NULL 			-- Адрес нового гостя (необязательно).
) RETURNS INTEGER AS $$
DECLARE
    new_id 				INTEGER; 					-- Переменная для хранения ID новой записи.
BEGIN
    INSERT INTO guests (passport_number, first_name, last_name, phone, email, address)
    VALUES (p_passport, p_first_name, p_last_name, p_phone, p_email, p_address)
    RETURNING guest_id INTO new_id; -- Вставляет данные и возвращает сгенерированный guest_id.
    
    RETURN new_id; -- Возвращает ID нового гостя.
END;
$$ LANGUAGE plpgsql;

-- Функция 'update_guest'
-- Обновляет информацию о существующем госте.
-- Параметры с DEFAULT NULL позволяют обновлять только указанные поля.
CREATE OR REPLACE FUNCTION update_guest(
    p_guest_id 			INTEGER, 					-- Идентификатор гостя, которого нужно обновить.
    p_first_name 		VARCHAR(50) DEFAULT NULL, 	-- Новое имя гостя (если указано).
    p_last_name 		VARCHAR(50) DEFAULT NULL, 	-- Новая фамилия гостя (если указано).
    p_phone 			VARCHAR(20) DEFAULT NULL, 	-- Новый телефон гостя (если указано).
    p_email 			VARCHAR(100) DEFAULT NULL, 	-- Новый email гостя (если указано).
    p_address 			TEXT DEFAULT NULL 			-- Новый адрес гостя (если указано).
) RETURNS VOID AS $$
BEGIN
    UPDATE guests
    SET 
        first_name = COALESCE(p_first_name, first_name), -- Если p_first_name не NULL, использовать его, иначе оставить текущее значение.
        last_name = COALESCE(p_last_name, last_name),
        phone = COALESCE(p_phone, phone),
        email = COALESCE(p_email, email),
        address = COALESCE(p_address, address)
    WHERE guest_id = p_guest_id; -- Обновляем запись по guest_id.
END;
$$ LANGUAGE plpgsql;

-- Функция 'delete_guest'
-- Удаляет запись о госте по его идентификатору.
CREATE OR REPLACE FUNCTION delete_guest(p_guest_id INTEGER) RETURNS VOID AS $$
BEGIN
    DELETE FROM guests WHERE guest_id = p_guest_id; -- Удаляет запись из таблицы guests.
END;
$$ LANGUAGE plpgsql;
