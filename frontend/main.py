import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget,
    QLineEdit, QLabel, QFormLayout, QMessageBox
)

# URL вашего Flask-сервера
BASE_URL = "http://localhost:5000/api/rooms"

class HotelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система управления гостиницей")
        self.setGeometry(100, 100, 400, 400)

        # Главный виджет и layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Список номеров
        self.room_list = QListWidget()
        self.layout.addWidget(QLabel("Список номеров:"))
        self.layout.addWidget(self.room_list)

        # Форма для добавления нового номера
        self.form_layout = QFormLayout()
        self.number_input = QLineEdit()
        self.type_input = QLineEdit()
        self.available_input = QLineEdit()
        self.form_layout.addRow("Номер:", self.number_input)
        self.form_layout.addRow("Тип:", self.type_input)
        self.form_layout.addRow("Доступность (True/False):", self.available_input)
        self.layout.addLayout(self.form_layout)

        # Кнопки
        self.add_button = QPushButton("Добавить номер")
        self.refresh_button = QPushButton("Обновить список")
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.refresh_button)

        # Привязка событий
        self.add_button.clicked.connect(self.add_room)
        self.refresh_button.clicked.connect(self.load_rooms)

        # Загрузка данных при запуске
        self.load_rooms()

    def load_rooms(self):
        """Загружает список номеров с сервера."""
        try:
            response = requests.get(BASE_URL)
            response.raise_for_status()  # Проверка на ошибки HTTP
            rooms = response.json()

            self.room_list.clear()
            for room in rooms:
                status = "✅" if room["available"] else "❌"
                item_text = f"{room['number']} ({room['type']}) - {status}"
                self.room_list.addItem(item_text)
        except requests.RequestException as e:
            self.show_error(f"Ошибка при загрузке данных: {e}")

    def add_room(self):
        """Добавляет новый номер на сервер."""
        number = self.number_input.text().strip()
        room_type = self.type_input.text().strip()
        available = self.available_input.text().strip()

        if not number or not room_type or not available:
            self.show_error("Все поля должны быть заполнены.")
            return

        try:
            available_bool = available.lower() == "true"
            new_room = {
                "number": number,
                "type": room_type,
                "available": available_bool
            }
            response = requests.post(BASE_URL, json=new_room)
            response.raise_for_status()

            self.show_message("Номер успешно добавлен!")
            self.clear_form()
            self.load_rooms()  # Обновляем список
        except requests.RequestException as e:
            self.show_error(f"Ошибка при добавлении номера: {e}")

    def clear_form(self):
        """Очищает поля ввода."""
        self.number_input.clear()
        self.type_input.clear()
        self.available_input.clear()

    def show_message(self, message):
        """Показывает информационное сообщение."""
        QMessageBox.information(self, "Информация", message)

    def show_error(self, message):
        """Показывает сообщение об ошибке."""
        QMessageBox.critical(self, "Ошибка", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HotelApp()
    window.show()
    sys.exit(app.exec())