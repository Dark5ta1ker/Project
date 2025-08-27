import requests

BASE_URL = "http://localhost:5000"


class ApiClient:
    def __init__(self, base_url=BASE_URL, timeout=10):
        self.base_url = base_url
        self.timeout = timeout

    # ===== НОМЕРА =====
    def get_rooms(self, params):
        """Получение списка номеров по фильтрам"""
        url = f"{self.base_url}/api/rooms/search"
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_room_by_number(self, room_number):
        """Поиск номера по его номеру"""
        url = f"{self.base_url}/api/rooms"
        response = requests.get(url, params={"room_number": room_number}, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_room_full_info(self, room_number: int):
        """Получение полной информации о номере"""
        url = f"{self.base_url}/api/rooms/{room_number}/full-info"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    # ===== БРОНИ =====
    def book_room(self, booking_data):
        """Создание бронирования"""
        url = f"{self.base_url}/api/bookings"
        response = requests.post(
            url,
            json=booking_data,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    # ===== УСЛУГИ =====
    def get_services(self, start_date, end_date):
        """Получение списка услуг за период"""
        url = f"{self.base_url}/ui/services-by-date"
        response = requests.get(
            url,
            params={"start_date": start_date, "end_date": end_date},
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()
