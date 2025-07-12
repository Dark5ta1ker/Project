from PyQt5 import QtCore, QtGui, QtWidgets
import requests

class RoomInfoWindow(QtWidgets.QDialog):
    def __init__(self, room_number, parent=None):
        super().__init__(parent)
        self.room_number = room_number
        self.setWindowTitle(f"Информация о номере {room_number}")
        self.resize(800, 600)

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)

        self.header = QtWidgets.QLabel(f"Подробная информация о номере {self.room_number}")
        self.header.setStyleSheet("font: bold 16pt 'Arial'; color: #0C5FFF;")
        self.layout.addWidget(self.header)

        self.tabs = QtWidgets.QTabWidget()

        # Вкладка 1: Основная информация
        self.basic_info_tab = QtWidgets.QWidget()
        self.basic_layout = QtWidgets.QFormLayout(self.basic_info_tab)
        self.tabs.addTab(self.basic_info_tab, "Основная информация")

        # Вкладка 2: Бронирования
        self.bookings_tab = QtWidgets.QWidget()
        self.bookings_layout = QtWidgets.QVBoxLayout(self.bookings_tab)
        self.bookings_table = QtWidgets.QTableView()
        self.bookings_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.bookings_layout.addWidget(self.bookings_table)
        self.tabs.addTab(self.bookings_tab, "Бронирования")

        # Вкладка 3: Обслуживание
        self.service_tab = QtWidgets.QWidget()
        self.service_layout = QtWidgets.QVBoxLayout(self.service_tab)
        self.service_table = QtWidgets.QTableView()
        self.service_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.service_layout.addWidget(self.service_table)
        self.tabs.addTab(self.service_tab, "Обслуживание")

        self.layout.addWidget(self.tabs)

        self.close_button = QtWidgets.QPushButton("Закрыть")
        self.close_button.setFixedSize(100, 30)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #0C5FFF;
                color: white;
                font: bold 11pt 'Arial';
                border-radius: 4px;
            }
        """)
        self.close_button.clicked.connect(self.close)
        self.layout.addWidget(self.close_button, alignment=QtCore.Qt.AlignRight)

    def load_data(self):
        try:
            self.show_loading(True)

            response = requests.get(
                f"http://localhost:5000/api/rooms/{self.room_number}/full-info",
                timeout=5
            )
            response.raise_for_status()
            room_data = response.json()

            self.fill_basic_info(room_data.get('room_info', {}))
            self.fill_bookings_table(room_data.get('bookings', []))
            self.fill_service_table(room_data.get('cleaning', []))

        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка соединения",
                f"Не удалось получить данные с сервера: {str(e)}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Ошибка",
                f"Ошибка обработки данных: {str(e)}"
            )
        finally:
            self.show_loading(False)

    def show_loading(self, show):
        if show:
            self.loading_indicator = QtWidgets.QProgressDialog(self)
            self.loading_indicator.setWindowTitle("Загрузка данных")
            self.loading_indicator.setLabelText("Получение информации о номере...")
            self.loading_indicator.setCancelButton(None)
            self.loading_indicator.setRange(0, 0)
            self.loading_indicator.show()
        elif hasattr(self, 'loading_indicator'):
            self.loading_indicator.close()

    def fill_basic_info(self, data):
        fields = [
            ("Тип номера", data.get('type', 'N/A')),
            ("Вместимость", str(data.get('capacity', 'N/A'))),
            ("Статус", data.get('status', 'N/A')),
            ("Цена за сутки", f"{data.get('daily_rate', 0):,.2f} ₽"),
            ("Описание", data.get('description', 'Нет описания'))
        ]

        for label, value in fields:
            label_widget = QtWidgets.QLabel(label + ":")
            value_widget = QtWidgets.QLabel(value)
            self.basic_layout.addRow(label_widget, value_widget)

    def fill_bookings_table(self, bookings):
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(["Гость", "Заезд", "Выезд", "Статус"])

        for booking in bookings:
            row = [
                QtGui.QStandardItem(booking.get('guest_name', 'N/A')),
                QtGui.QStandardItem(booking.get('check_in', 'N/A')),
                QtGui.QStandardItem(booking.get('check_out', 'N/A')),
                QtGui.QStandardItem(booking.get('status', 'N/A'))
            ]
            model.appendRow(row)

        self.bookings_table.setModel(model)
        self.bookings_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def fill_service_table(self, cleaning_records):
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(["Дата уборки", "Статус"])

        for record in cleaning_records:
            row = [
                QtGui.QStandardItem(record.get('date', 'N/A')),
                QtGui.QStandardItem("Требуется" if record.get('needs_cleaning') else "Не требуется")
            ]
            model.appendRow(row)

        self.service_table.setModel(model)
        self.service_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
