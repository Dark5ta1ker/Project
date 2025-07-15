-- Таблица 'guests' (Гости)
-- Хранит основную информацию о каждом госте отеля.
CREATE TABLE guests (
    guest_id 			SERIAL PRIMARY KEY, 								-- Уникальный идентификатор гостя. SERIAL автоматически генерирует последовательные числа.
    passport_number 	VARCHAR(20) NOT NULL UNIQUE, 						-- Номер паспорта гостя. Обязательное поле, должно быть уникальным для каждого гостя.
    first_name 			VARCHAR(50) NOT NULL, 								-- Имя гостя. Обязательное поле.
    last_name 			VARCHAR(50) NOT NULL, 								-- Фамилия гостя. Обязательное поле.
    phone 				VARCHAR(20) NOT NULL, 								-- Контактный телефон гостя. Обязательное поле.
    email 				VARCHAR(100), 										-- Адрес электронной почты гостя (необязательно).
    address 			TEXT, 												-- Адрес проживания гостя (необязательно).
    created_at 			TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Дата и время создания записи о госте. Устанавливается автоматически при вставке.
    updated_at 			TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Дата и время последнего обновления записи о госте. Обновляется триггером.
    CONSTRAINT valid_passport CHECK (passport_number ~ '^[0-9]{6,20}$'), -- Ограничение: номер паспорта должен состоять из букв и цифр, длиной от 6 до 20 символов.
    CONSTRAINT valid_email CHECK (email IS NULL OR email ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$') -- Ограничение: email должен быть NULL или соответствовать формату email.
);

-- Таблица 'rooms' (Номера)
-- Содержит информацию о каждом номере в отеле.
CREATE TABLE rooms (
    room_id 			SERIAL PRIMARY KEY, 			  -- Уникальный идентификатор номера.
    room_number 		VARCHAR(10) NOT NULL UNIQUE, 	  -- Номер комнаты (например, "101"). Обязательное поле, должно быть уникальным.
    type 				room_type NOT NULL, 			  -- Тип номера (использует пользовательский тип room_type).
    capacity 			SMALLINT NOT NULL, 				  -- Максимальная вместимость номера (количество человек).
    daily_rate 			DECIMAL(10, 2) NOT NULL, 		  -- Ежедневная стоимость проживания в номере.
    status 				room_status DEFAULT 'available',  -- Текущий статус номера (использует пользовательский тип room_status), по умолчанию 'available'.
    description 		TEXT, 							  -- Описание номера (например, "с видом на море").
    CONSTRAINT positive_rate CHECK (daily_rate > 0), 	  -- Ограничение: ежедневная ставка должна быть больше нуля.
    CONSTRAINT valid_capacity CHECK (capacity BETWEEN 1 AND 6) -- Ограничение: вместимость номера должна быть от 1 до 6 человек.
);

-- Таблица 'bookings' (Бронирования)
-- Записывает информацию о бронированиях номеров гостями.
CREATE TABLE bookings (
    booking_id 			SERIAL PRIMARY KEY, 								-- Уникальный идентификатор бронирования.
    guest_id 			INTEGER NOT NULL REFERENCES guests(guest_id), 		-- Ссылка на ID гостя, который сделал бронирование (внешний ключ).
    room_id 			INTEGER NOT NULL REFERENCES rooms(room_id), 		-- Ссылка на ID номера, который был забронирован (внешний ключ).
    check_in_date 		DATE NOT NULL, 										-- Дата заезда.
    check_out_date 		DATE NOT NULL, 										-- Дата выезда.
    status 				booking_status DEFAULT 'confirmed', 				-- Текущий статус бронирования (использует пользовательский тип booking_status), по умолчанию 'confirmed'.
    adults 				SMALLINT NOT NULL DEFAULT 1, 						-- Количество взрослых в бронировании.
    children 			SMALLINT NOT NULL DEFAULT 0, 						-- Количество детей в бронировании.
    created_at 			TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Дата и время создания записи о бронировании.
    CONSTRAINT valid_dates CHECK (check_out_date > check_in_date), 			-- Ограничение: дата выезда должна быть строго позже даты заезда.
    CONSTRAINT valid_occupants CHECK (adults + children > 0) 				-- Ограничение: общее количество проживающих (взрослых + детей) должно быть больше нуля.
);

-- Таблица 'services' (Услуги)
-- Список дополнительных услуг, предлагаемых отелем.
CREATE TABLE services (
    service_id 			SERIAL PRIMARY KEY, 	 -- Уникальный идентификатор услуги.
    name 				VARCHAR(100) NOT NULL, 	 -- Название услуги (например, "Завтрак", "Прачечная").
    description 		TEXT, 					 -- Подробное описание услуги.
    price 				DECIMAL(10, 2) NOT NULL, -- Стоимость услуги.
    is_active 			BOOLEAN DEFAULT TRUE, 	 -- Флаг, указывающий, активна ли услуга в данный момент.
    CONSTRAINT positive_price CHECK (price >= 0) -- Ограничение: цена услуги не может быть отрицательной.
);

-- Таблица 'booking_services' (Услуги бронирования)
-- Связующая таблица для связи бронирований с оказанными услугами.
-- Позволяет отслеживать, какие услуги были заказаны для каждого бронирования.
CREATE TABLE booking_services (
    booking_service_id 	SERIAL PRIMARY KEY, 							  -- Уникальный идентификатор записи об услуге для бронирования.
    booking_id 			INTEGER NOT NULL REFERENCES bookings(booking_id), -- Ссылка на ID бронирования (внешний ключ).
    service_id 			INTEGER NOT NULL REFERENCES services(service_id), -- Ссылка на ID услуги (внешний ключ).
    quantity 			SMALLINT NOT NULL DEFAULT 1, 					  -- Количество заказанной услуги.
    service_date 		DATE NOT NULL DEFAULT CURRENT_DATE, 			  -- Дата оказания услуги.
    notes 				TEXT, 											  -- Дополнительные примечания к оказанной услуге.
    CONSTRAINT positive_quantity CHECK (quantity > 0) 					  -- Ограничение: количество услуги должно быть больше нуля.
);

-- Таблица 'payments' (Платежи)
-- Записывает все финансовые транзакции, связанные с бронированиями.
CREATE TABLE payments (
    payment_id 			SERIAL PRIMARY KEY, 							  	-- Уникальный идентификатор платежа.
    booking_id 			INTEGER NOT NULL REFERENCES bookings(booking_id), 	-- Ссылка на ID бронирования, к которому относится платеж (внешний ключ).
    amount 				DECIMAL(10, 2) NOT NULL, 					      	-- Сумма платежа.
    method 				payment_method NOT NULL, 							-- Метод оплаты (использует пользовательский тип payment_method).
    status 				payment_status DEFAULT 'pending', 					-- Статус платежа (использует пользовательский тип payment_status), по умолчанию 'pending'.
    transaction_date 	TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP, -- Дата и время совершения транзакции.
    notes 				TEXT, 												-- Дополнительные примечания к платежу.
    CONSTRAINT positive_amount CHECK (amount > 0) 							-- Ограничение: сумма платежа должна быть больше нуля.
);
