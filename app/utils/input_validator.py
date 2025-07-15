import re
from datetime import datetime

class InputValidator:
    """
    Класс для санитизации (очистки) входных данных от потенциально опасных паттернов.
    Не заменяет валидацию на уровне БД или бизнес-логики.
    """
    XSS_PATTERNS = [
        r"<script.*?>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
    ]

    SQL_INJECTION_PATTERNS = [
        r"['\"].*\b(OR|AND)\b.*['\"]",
        r";--",
        r"UNION\s+SELECT",
        r"DROP\s+TABLE",
        r"DELETE\s+FROM",
    ]

    @classmethod
    def sanitize_input(cls, data):
        """
        Рекурсивно очищает входные данные от потенциально опасных паттернов.
        Возвращает очищенные данные без изменения структуры.
        """
        if isinstance(data, dict):
            return {k: cls.sanitize_input(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls.sanitize_input(item) for item in data]
        elif isinstance(data, str):
            for pattern in cls.XSS_PATTERNS + cls.SQL_INJECTION_PATTERNS:
                data = re.sub(pattern, '', data, flags=re.IGNORECASE)
            return data
        return data

    @classmethod
    def validate_dates(cls, date_str, format="%Y-%m-%d"):
        """
        Валидация дат без санитизации (отдельный метод)
        """
        try:
            datetime.strptime(date_str, format)
            return True
        except (ValueError, TypeError):
            return False

    @classmethod
    def validate_phone(cls, phone_str):
        """Валидация номера телефона (пример)"""
        return bool(re.match(r'^\+?[\d\s\-\(\)]{7,15}$', str(phone_str)))