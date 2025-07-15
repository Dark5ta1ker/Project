import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    """
    Настройка логгера для приложения.
    """
    # Создание логгера
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Устанавливаем глобальный уровень логов

    # Форматтер для логов
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # Логирование в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Выводим INFO и выше в консоль
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Логирование в файл
    file_handler = RotatingFileHandler(
        "app.log", maxBytes=1024 * 1024, backupCount=5
    )  # Лог-файл размером до 1 МБ, хранятся 5 старых файлов
    file_handler.setLevel(logging.DEBUG)  # Сохраняем DEBUG и выше в файл
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger