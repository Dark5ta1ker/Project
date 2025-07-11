-- 3. ТРИГГЕРЫ ДЛЯ АВТОМАТИЧЕСКОГО ОБНОВЛЕНИЯ ПОЛЯ UPDATED_AT

-- Функция 'update_timestamp()'
-- Эта функция PL/pgSQL будет вызываться триггером для обновления поля 'updated_at' в таблицах.
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP; -- Устанавливает значение 'updated_at' новой (изменяемой) записи на текущее время.
    RETURN NEW; -- Возвращает измененную запись.
END;
$$ LANGUAGE plpgsql; -- Указывает, что функция написана на языке PL/pgSQL.
