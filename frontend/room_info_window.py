from PyQt5 import QtCore, QtGui, QtWidgets
import requests

class RoomInfoWindow(QtWidgets.QDialog):
    def __init__(self, room_number, parent=None):
        """
        Конструктор окна информации о номере.
        :param room_number: Номер комнаты, для которой отображается информация.
        :param parent: Родительский виджет (если есть).
        """
        super().__init__(parent)  # Инициализация родительского класса
        self.room_number = room_number  # Сохраняем номер комнаты
        self.setWindowTitle(f"Информация о номере {room_number}")  # Устанавливаем заголовок окна
        self.resize(800, 600)  # Размер окна

        self.setup_ui()  # Настройка интерфейса
        self.load_data()  # Загрузка данных о номере

    def setup_ui(self):
        """
        Настройка пользовательского интерфейса окна.
        """
        self.layout = QtWidgets.QVBoxLayout(self)  # Основной вертикальный layout

        # Заголовок
        self.header = QtWidgets.QLabel(f"Подробная информация о номере {self.room_number}")
        self.header.setStyleSheet("font: bold 16pt 'Arial'; color: #0C5FFF;")  # Стиль текста
        self.layout.addWidget(self.header)

        # Вкладки (табы)
        self.tabs = QtWidgets.QTabWidget()

        # ----- Вкладка "Основная информация" -----
        self.basic_info_tab = QtWidgets.QWidget()
        self.basic_layout = QtWidgets.QFormLayout(self.basic_info_tab)  # Форматная сетка для основной информации
        self.tabs.addTab(self.basic_info_tab, "Основная информация")

        # ----- Вкладка "Бронирования" -----
        self.bookings_tab = QtWidgets.QWidget()
        self.bookings_layout = QtWidgets.QVBoxLayout(self.bookings_tab)  # Вертикальный layout для бронирований
        self.bookings_table = QtWidgets.QTableView()  # Таблица для отображения бронирований
        self.bookings_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Отключение редактирования
        self.bookings_layout.addWidget(self.bookings_table)
        self.tabs.addTab(self.bookings_tab, "Бронирования")

        # ----- Вкладка "Обслуживание" -----
        self.service_tab = QtWidgets.QWidget()
        self.service_layout = QtWidgets.QVBoxLayout(self.service_tab)  # Вертикальный layout для обслуживания
        self.service_table = QtWidgets.QTableView()  # Таблица для отображения услуг и уборки
        self.service_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Отключение редактирования
        self.service_layout.addWidget(self.service_table)
        self.tabs.addTab(self.service_tab, "Обслуживание")

        # ----- Вкладка "Оплата" -----
        self.payments_tab = QtWidgets.QWidget()
        self.payments_layout = QtWidgets.QVBoxLayout(self.payments_tab)  # Вертикальный layout для оплат
        self.payments_table = QtWidgets.QTableView()  # Таблица для отображения платежей
        self.payments_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # Отключение редактирования
        self.payments_layout.addWidget(self.payments_table)
        self.tabs.addTab(self.payments_tab, "Оплата")

        self.layout.addWidget(self.tabs)  # Добавляем табы в основной layout

        # Кнопка закрытия
        self.close_button = QtWidgets.QPushButton("Закрыть")
        self.close_button.setFixedSize(100, 30)  # Размер кнопки
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #0C5FFF;
                color: white;
                font: bold 11pt 'Arial';
                border-radius: 4px;
            }
        """)  # Стиль кнопки
        self.close_button.clicked.connect(self.close)  # Привязка действия к кнопке
        self.layout.addWidget(self.close_button, alignment=QtCore.Qt.AlignRight)  # Выравнивание справа

    def load_data(self):
        """
        Загрузка данных о номере с сервера.
        """
        try:
            self.show_loading(True)  # Показываем индикатор загрузки

            # Запрос данных с сервера
            response = requests.get(f"http://localhost:5000/api/rooms/{self.room_number}/full-info", timeout=5)
            response.raise_for_status()  # Проверка статуса ответа
            room_data = response.json()  # Парсинг JSON-ответа

            # Заполнение данных во вкладках
            self.fill_basic_info(room_data.get('room_info', {}))  # Основная информация
            self.fill_bookings_table(room_data.get('bookings', []))  # Бронирования
            self.fill_service_table(room_data.get('cleaning', []), room_data.get('services', []))  # Обслуживание
            self.fill_payments_table(room_data.get('payments', []))  # Оплата

        except requests.exceptions.RequestException as e:
            # Обработка ошибок соединения
            QtWidgets.QMessageBox.warning(self, "Ошибка соединения", f"Не удалось получить данные с сервера: {str(e)}")
        except Exception as e:
            # Обработка других ошибок
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Ошибка обработки данных: {str(e)}")
        finally:
            self.show_loading(False)  # Скрываем индикатор загрузки

    def show_loading(self, show):
        """
        Показывает или скрывает индикатор загрузки.
        :param show: True - показать, False - скрыть.
        """
        if show:
            self.loading_indicator = QtWidgets.QProgressDialog(self)
            self.loading_indicator.setWindowTitle("Загрузка данных")
            self.loading_indicator.setLabelText("Получение информации о номере...")
            self.loading_indicator.setCancelButton(None)  # Отключаем кнопку отмены
            self.loading_indicator.setRange(0, 0)  # Бесконечный прогресс
            self.loading_indicator.show()
        elif hasattr(self, 'loading_indicator'):
            self.loading_indicator.close()

    def fill_basic_info(self, data):
        """
        Заполняет вкладку "Основная информация".
        :param data: Словарь с данными о номере.
        """
        status_map = {
            'available': 'Свободен',
            'occupied': 'Занят',
            'maintenance': 'На обслуживании',
            'confirmed': 'Подтверждено',
            'checked_in': 'Заселен',
            'checked_out': 'Выписан',
            'cancelled': 'Отменен'
        }

        type_map = {
            'Basic': 'Базовый',
            'Advanced': 'Продвинутый',
            'Business': 'Бизнес',
            'Dorm': 'Общий'
        }

        fields = [
            ("Тип номера", type_map.get(data.get('type', ''), data.get('type', 'N/A'))),
            ("Вместимость", str(data.get('capacity', 'N/A'))),
            ("Статус", status_map.get(data.get('status', ''), data.get('status', 'N/A'))),
            ("Цена за сутки", f"{data.get('daily_rate', 0):,.2f} ₽"),
            ("Описание", data.get('description', 'Нет описания'))
        ]

        # Добавление полей в форму
        for label, value in fields:
            label_widget = QtWidgets.QLabel(label + ":")
            label_widget.setStyleSheet("font: bold 12pt 'Arial'; color: #333;")
            value_widget = QtWidgets.QLabel(value)
            value_widget.setStyleSheet("font: 12pt 'Arial'; color: #222;")
            self.basic_layout.addRow(label_widget, value_widget)

    def fill_bookings_table(self, bookings):
        """
        Заполняет таблицу бронирований.
        :param bookings: Список словарей с данными о бронированиях.
        """
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(["Гость", "Заезд", "Выезд", "Статус"])

        status_map = {
            'confirmed': 'Подтверждено',
            'checked_in': 'Заселен',
            'checked_out': 'Выписан',
            'cancelled': 'Отменен'
        }

        # Заполнение строк таблицы
        for booking in bookings:
            status = booking.get('status', 'N/A')
            row = [
                QtGui.QStandardItem(booking.get('guest_name', 'N/A')),
                QtGui.QStandardItem(booking.get('check_in', 'N/A')),
                QtGui.QStandardItem(booking.get('check_out', 'N/A')),
                QtGui.QStandardItem(status_map.get(status, status))
            ]
            model.appendRow(row)

        self.bookings_table.setModel(model)
        self.bookings_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def fill_service_table(self, cleaning_records, extra_services):
        """
        Заполняет таблицу обслуживания (уборка + услуги).
        :param cleaning_records: Список записей об уборке.
        :param extra_services: Список дополнительных услуг.
        """
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(["Дата", "Название", "Описание", "Дополнительно"])

        # Записи об уборке
        for record in cleaning_records:
            row = [
                QtGui.QStandardItem(record.get('date', '—')),
                QtGui.QStandardItem("Уборка"),
                QtGui.QStandardItem("Ежедневная уборка"),
                QtGui.QStandardItem("Требуется" if record.get('needs_cleaning') else "Не требуется")
            ]
            model.appendRow(row)

        # Дополнительные услуги
        for service in extra_services:
            row = [
                QtGui.QStandardItem(service.get('date', '—')),
                QtGui.QStandardItem(service.get('service_name', '—')),
                QtGui.QStandardItem(f"×{service.get('quantity', 1)}"),
                QtGui.QStandardItem(service.get('notes', ''))
            ]
            model.appendRow(row)

        self.service_table.setModel(model)
        self.service_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def fill_payments_table(self, payments):
        """
        Заполняет таблицу платежей.
        :param payments: Список словарей с данными о платежах.
        """
        model = QtGui.QStandardItemModel()
        model.setHorizontalHeaderLabels(["Дата", "Сумма", "Статус", "Способ оплаты"])

        status_map = {
            'pending': 'В ожидании',
            'completed': 'Завершен',
            'failed': 'Ошибка',
            'refunded': 'Возврат'
        }

        method_map = {
            'cash': 'Наличные',
            'credit_card': 'Кредитная карта',
            'debit_card': 'Дебетовая карта',
            'bank_transfer': 'Банковский перевод',
            'online': 'Онлайн-платеж'
        }

        # Заполнение строк таблицы
        for payment in payments:
            row = [
                QtGui.QStandardItem(payment.get('date', 'N/A')),
                QtGui.QStandardItem(f"{payment.get('amount', 0):,.2f} ₽"),
                QtGui.QStandardItem(status_map.get(payment.get('status', ''), payment.get('status', ''))),
                QtGui.QStandardItem(method_map.get(payment.get('method', ''), payment.get('method', '')))
            ]
            model.appendRow(row)

        self.payments_table.setModel(model)
        self.payments_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)