import re

class InputValidator:
    """
    Класс для проверки входных данных на наличие опасных паттернов.
    """
    # Регулярные выражения для обнаружения подозрительных паттернов
    XSS_PATTERNS = [
        r"<script.*?>.*?</script>",  # Проверка на теги <script>
        r"javascript:",              # Проверка на JavaScript в атрибутах
        r"on\w+\s*=",                # Проверка на события (onclick, onload и т.д.)
    ]

    SQL_INJECTION_PATTERNS = [
        r"['\"].*\b(OR|AND)\b.*['\"]",  # Проверка на логические операторы в SQL-инъекциях
        r";--",                         # Проверка на комментарии SQL
        r"UNION\s+SELECT",              # Проверка на UNION-инъекции
        r"DROP\s+TABLE",                # Проверка на DROP TABLE
        r"DELETE\s+FROM",               # Проверка на DELETE FROM
    ]

    @staticmethod
    def is_safe_input(data):
        """
        Проверяет, является ли входное значение безопасным.
        :param data: Входные данные (строка или словарь).
        :return: True, если данные безопасны, иначе False.
        """
        if isinstance(data, dict):
            # Если данные - словарь, проверяем каждое значение
            for value in data.values():
                if not InputValidator.is_safe_input(value):
                    return False
            return True
        elif isinstance(data, list):
            # Если данные - список, проверяем каждый элемент
            for item in data:
                if not InputValidator.is_safe_input(item):
                    return False
            return True
        elif isinstance(data, str):
            # Если данные - строка, проверяем на наличие опасных паттернов
            for pattern in InputValidator.XSS_PATTERNS + InputValidator.SQL_INJECTION_PATTERNS:
                if re.search(pattern, data, re.IGNORECASE):
                    return False
            return True
        else:
            # Для всех остальных типов данных считаем их безопасными
            return True