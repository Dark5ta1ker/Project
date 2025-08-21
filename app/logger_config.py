import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app=None):
    """
    Настройка логгера для приложения.
    """
    # Создание логгера
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Глобальный уровень логов

    # Если хендлеры уже есть — не добавляем повторно
    if logger.handlers:
        return logger

    # Форматтер для логов
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )

    # Консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Файл
    file_handler = RotatingFileHandler(
        "app.log", maxBytes=1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Если передали Flask app — привязываем уровень логирования
    if app:
        log_level = app.config.get("LOG_LEVEL", "INFO")
        app.logger.setLevel(log_level)

    return logger
