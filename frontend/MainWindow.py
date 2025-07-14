from PyQt5 import QtCore, QtGui, QtWidgets
from room_info_window import RoomInfoWindow  # Импортируем окно информации о номере
from booking import GuestBookingDialog  # Импортируем диалог бронирования
import requests  # Для HTTP-запросов
import traceback  # Для отладки ошибок

# Класс делегата для кастомной отрисовки ячеек таблицы
class TableItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        """
        Отрисовка ячеек таблицы с градиентом и выделением.
        """
        if option.state & QtWidgets.QStyle.State_Selected:
            # Если строка выделена - сплошной цвет
            painter.fillRect(option.rect, QtGui.QColor(10, 80, 200))
        else:
            # Для обычных строк - вертикальный градиент
            gradient = QtGui.QLinearGradient(option.rect.topLeft(), option.rect.bottomLeft())
            gradient.setColorAt(0, QtGui.QColor(240, 240, 240))
            gradient.setColorAt(0.5, QtGui.QColor(250, 250, 250))
            gradient.setColorAt(1, QtGui.QColor(240, 240, 240))
            painter.fillRect(option.rect, gradient)
        
        # Отрисовка текста
        painter.save()
        text_color = QtCore.Qt.white if option.state & QtWidgets.QStyle.State_Selected else QtCore.Qt.black
        painter.setPen(text_color)
        text = index.data(QtCore.Qt.DisplayRole)
        if text is not None:
            painter.drawText(option.rect, QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter, str(text))
        painter.restore()

    def sizeHint(self, option, index):
        """
        Устанавливает высоту строки таблицы.
        """
        size = super().sizeHint(option, index)
        size.setHeight(40)  # Фиксированная высота строки
        return size

    def createEditor(self, parent, option, index):
        """
        Отключает редактирование ячеек таблицы.
        """
        return None

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        """
        Настройка главного окна приложения.
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)  # Размер окна
        MainWindow.setStyleSheet("QMainWindow { background-color: #f5f5f5; }")  # Цвет фона
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.main_window = MainWindow

        # Главный макет окна
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

        # Заголовок
        self.header = QtWidgets.QLabel("Система управления отелем")
        self.header.setStyleSheet("""
            QLabel {
                background-color: #0C5FFF;
                color: white;
                font: bold 18pt 'Arial';
                padding: 15px;
                border-radius: 5px;
            }
        """)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setFixedHeight(70)
        main_layout.addWidget(self.header)

        # Вкладки (таблицы)
        self.setup_rooms_tab()  # Настройка вкладки "Номера"
        main_layout.addWidget(self.tabWidget)

        # Нижняя панель с кнопками
        self.setup_bottom_panel()
        main_layout.addWidget(self.bottom_panel)

        # Установка центрального виджета
        MainWindow.setCentralWidget(self.centralwidget)

        # Подключение сигналов
        self.connect_signals()

    def setup_rooms_tab(self):
        """
        Настройка вкладки "Номера".
        """
        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setStyleSheet("""
            /* Стили для вкладок */
        """)

        # ----- Вкладка "Номера" -----
        self.rooms_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.rooms_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Панель фильтров
        filter_panel = QtWidgets.QGroupBox("Фильтры поиска")
        filter_layout = QtWidgets.QGridLayout()
        filter_layout.setContentsMargins(15, 20, 15, 15)
        filter_layout.setHorizontalSpacing(20)
        filter_layout.setVerticalSpacing(15)

        # Компоненты фильтрации
        self.status_combo = self.create_combo_box(["Все", "Свободен", "Занят", "На обслуживании"])
        self.guests_combo = self.create_combo_box(["1", "2", "3", "4+"])
        self.check_in_date = self.create_date_edit()
        self.check_out_date = self.create_date_edit()
        self.check_out_date.setDate(QtCore.QDate.currentDate().addDays(1))

        # Кнопка поиска
        self.search_button = QtWidgets.QPushButton("Поиск")
        self.search_button.setFixedHeight(40)
        self.search_button.clicked.connect(self.fetch_rooms_data)

        # Размещение элементов фильтрации
        filter_layout.addWidget(QtWidgets.QLabel("Статус номера:"), 0, 0)
        filter_layout.addWidget(self.status_combo, 1, 0)
        filter_layout.addWidget(QtWidgets.QLabel("Количество гостей:"), 0, 1)
        filter_layout.addWidget(self.guests_combo, 1, 1)
        filter_layout.addWidget(QtWidgets.QLabel("Дата заезда:"), 0, 2)
        filter_layout.addWidget(self.check_in_date, 1, 2)
        filter_layout.addWidget(QtWidgets.QLabel("Дата выезда:"), 0, 3)
        filter_layout.addWidget(self.check_out_date, 1, 3)
        filter_layout.addWidget(self.search_button, 1, 4)

        filter_panel.setLayout(filter_layout)
        layout.addWidget(filter_panel)

        # Таблица номеров
        self.rooms_table = QtWidgets.QTableView()
        self.rooms_table.setObjectName("roomsTable")
        self.rooms_table.setStyleSheet("""
            /* Стили для таблицы */
        """)
        self.rooms_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.rooms_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.rooms_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.rooms_table.verticalHeader().setVisible(False)
        self.rooms_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.rooms_table.setItemDelegate(TableItemDelegate())
        self.rooms_table.setShowGrid(False)
        self.rooms_table.verticalHeader().setDefaultSectionSize(40)

        layout.addWidget(self.rooms_table)
        self.tabWidget.addTab(self.rooms_tab, "Номера")

        # ----- Вкладка "Услуги" -----
        self.service_tab = QtWidgets.QWidget()
        service_layout = QtWidgets.QVBoxLayout(self.service_tab)
        service_layout.setContentsMargins(10, 10, 10, 10)
        service_layout.setSpacing(15)

        # Панель фильтрации услуг
        service_filter_panel = QtWidgets.QGroupBox("Фильтр по дате")
        service_filter_layout = QtWidgets.QHBoxLayout(service_filter_panel)
        service_filter_layout.setContentsMargins(15, 10, 15, 10)

        self.service_start_date = self.create_date_edit()
        self.service_end_date = self.create_date_edit()
        self.service_end_date.setDate(QtCore.QDate.currentDate().addDays(1))

        self.service_filter_button = QtWidgets.QPushButton("Показать")
        self.service_filter_button.setFixedHeight(35)
        self.service_filter_button.clicked.connect(self.fetch_service_data)

        service_filter_layout.addWidget(QtWidgets.QLabel("С:"))
        service_filter_layout.addWidget(self.service_start_date)
        service_filter_layout.addWidget(QtWidgets.QLabel("По:"))
        service_filter_layout.addWidget(self.service_end_date)
        service_filter_layout.addStretch()
        service_filter_layout.addWidget(self.service_filter_button)

        service_layout.addWidget(service_filter_panel)

        # Таблица услуг
        self.service_table = QtWidgets.QTableView()
        self.service_table.setObjectName("serviceTable")
        self.service_table.setStyleSheet(self.rooms_table.styleSheet())
        self.service_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.service_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.service_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.service_table.verticalHeader().setVisible(False)
        self.service_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.service_table.setItemDelegate(TableItemDelegate())
        self.service_table.setShowGrid(False)
        self.service_table.verticalHeader().setDefaultSectionSize(40)

        service_layout.addWidget(self.service_table)
        self.tabWidget.addTab(self.service_tab, "Услуги")

    def setup_bottom_panel(self):
        """
        Настройка нижней панели с кнопками.
        """
        self.bottom_panel = QtWidgets.QFrame()
        self.bottom_panel.setStyleSheet("background-color: #f0f0f0; border-top: 1px solid #ddd;")
        bottom_layout = QtWidgets.QHBoxLayout(self.bottom_panel)
        bottom_layout.setContentsMargins(10, 5, 10, 5)

        # Кнопка "Инфо"
        self.info_button = QtWidgets.QPushButton("Инфо")
        self.info_button.setFixedSize(100, 30)
        self.info_button.setStyleSheet("""
            QPushButton {
                background-color: #0C5FFF;
                color: white;
                font: bold 11pt 'Arial';
                border-radius: 4px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.info_button.setEnabled(False)

        # Кнопка "Бронировать"
        self.book_button = QtWidgets.QPushButton("Бронировать")
        self.book_button.setFixedSize(120, 30)
        self.book_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font: bold 11pt 'Arial';
                border-radius: 4px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3e8e41; }
        """)
        self.book_button.setEnabled(False)

        bottom_layout.addWidget(self.info_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.book_button)

    def create_combo_box(self, items):
        """
        Создание выпадающего списка (ComboBox).
        """
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        combo.setStyleSheet("""
            /* Стили для ComboBox */
        """)
        combo.setFixedHeight(35)
        return combo

    def create_date_edit(self):
        """
        Создание поля выбора даты (DateEdit).
        """
        date_edit = QtWidgets.QDateEdit(calendarPopup=True)
        date_edit.setDate(QtCore.QDate.currentDate())
        date_edit.setDisplayFormat("dd.MM.yyyy")
        date_edit.setStyleSheet("""
            /* Стили для DateEdit */
        """)
        date_edit.setFixedHeight(35)
        return date_edit

    def connect_signals(self):
        """
        Подключение сигналов к слотам.
        """
        self.info_button.clicked.connect(self.show_room_info)
        self.book_button.clicked.connect(self.book_room)

        if self.rooms_table.selectionModel():
            self.rooms_table.selectionModel().selectionChanged.connect(self.on_room_selected)

    def on_room_selected(self, selected, deselected):
        """
        Обработка выбора строки в таблице номеров.
        """
        has_selection = len(selected.indexes()) > 0
        self.info_button.setEnabled(has_selection)

        if has_selection:
            row = selected.indexes()[0].row()
            status_item = self.rooms_table.model().index(row, 3)  # 3 - столбец статуса
            status = status_item.data()
            is_available = status == "Свободен"
            self.book_button.setEnabled(is_available)
        else:
            self.book_button.setEnabled(False)

    def show_room_info(self):
        """
        Отображение окна информации о номере.
        """
        selected = self.rooms_table.selectionModel().selectedRows()
        if not selected:
            return
        row = selected[0].row()
        room_number = self.rooms_table.model().index(row, 0).data()
        self.info_window = RoomInfoWindow(room_number, self.main_window)
        self.info_window.exec_()

    def fetch_rooms_data(self):
        """
        Получение данных о номерах с сервера.
        """
        try:
            check_in = self.check_in_date.date()
            check_out = self.check_out_date.date()
            if check_out <= check_in:
                QtWidgets.QMessageBox.warning(self.main_window, "Ошибка дат", "Дата выезда должна быть позже даты заезда")
                return

            params = {
                "check_in": check_in.toString("yyyy-MM-dd"),
                "check_out": check_out.toString("yyyy-MM-dd")
            }

            status = self.status_combo.currentText()
            if status != "Все":
                params["status"] = {
                    "Свободен": "available",
                    "Занят": "occupied",
                    "На обслуживании": "maintenance"
                }.get(status)

            guests = self.guests_combo.currentText()
            if guests == "4+":
                params["min_capacity"] = 4
            else:
                params["capacity"] = guests

            response = requests.get("http://localhost:5000/ui/rooms", params=params, timeout=10)
            response.raise_for_status()
            rooms_data = response.json()

            model = QtGui.QStandardItemModel()
            model.setHorizontalHeaderLabels(["Номер", "Тип", "Вместимость", "Статус", "Цена за сутки"])

            type_map = {
                'Basic': 'Базовый',
                'Advanced': 'Продвинутый',
                'Business': 'Бизнес',
                'Dorm': 'Общий'
            }

            for room in rooms_data:
                if not all(k in room for k in ['room_number', 'type', 'capacity', 'status', 'daily_rate']):
                    continue

                status = room.get('dynamic_status', room['status'])
                status_text = {
                    'available': 'Свободен',
                    'occupied': 'Занят',
                    'maintenance': 'На обслуживании'
                }.get(status, 'Неизвестно')

                row = [
                    QtGui.QStandardItem(str(room['room_number'])),
                    QtGui.QStandardItem(type_map.get(room['type'], room['type'])),
                    QtGui.QStandardItem(str(room['capacity'])),
                    QtGui.QStandardItem(status_text),
                    QtGui.QStandardItem(f"{room['daily_rate']:,.2f} ₽".replace(",", " "))
                ]
                model.appendRow(row)

            self.rooms_table.setModel(model)
            self.rooms_table.selectionModel().selectionChanged.connect(self.on_room_selected)
            self.info_button.setEnabled(False)
            self.book_button.setEnabled(False)

            if model.rowCount() == 0:
                QtWidgets.QMessageBox.information(self.main_window, "Результаты поиска", "Номера по заданным критериям не найдены")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Ошибка", f"Ошибка при загрузке данных:\n{str(e)}")

    def fetch_service_data(self):
        """
        Получение данных об услугах с сервера.
        """
        try:
            start_date = self.service_start_date.date().toString("yyyy-MM-dd")
            end_date = self.service_end_date.date().toString("yyyy-MM-dd")
            if self.service_start_date.date() >= self.service_end_date.date():
                QtWidgets.QMessageBox.warning(self.main_window, "Ошибка дат", "Дата окончания должна быть позже начала")
                return

            response = requests.get(
                "http://localhost:5000/ui/services-by-date",
                params={"start_date": start_date, "end_date": end_date},
                timeout=10
            )
            response.raise_for_status()
            services_data = response.json()

            model = QtGui.QStandardItemModel()
            model.setHorizontalHeaderLabels(["Дата", "Номер", "Услуга", "Кол-во", "Примечание"])

            for service in services_data:
                model.appendRow([
                    QtGui.QStandardItem(service.get("date", "—")),
                    QtGui.QStandardItem(str(service.get("room_number", "—"))),
                    QtGui.QStandardItem(service.get("service_name", "—")),
                    QtGui.QStandardItem(str(service.get("quantity", "—"))),
                    QtGui.QStandardItem(service.get("notes", ""))
                ])

            self.service_table.setModel(model)

            if model.rowCount() == 0:
                QtWidgets.QMessageBox.information(self.main_window, "Результаты", "Услуги за выбранный период не найдены.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.main_window, "Ошибка", f"Ошибка при загрузке услуг:\n{str(e)}")
            print(traceback.format_exc())

    def book_room(self):
        """
        Бронирование выбранного номера.
        """
        selected = self.rooms_table.selectionModel().selectedRows()
        if not selected:
            return

        row = selected[0].row()
        room_number = self.rooms_table.model().index(row, 0).data()
        capacity = int(self.rooms_table.model().index(row, 2).data())

        booking_dialog = GuestBookingDialog(room_number=room_number, room_capacity=capacity)
        if booking_dialog.exec_() == QtWidgets.QDialog.Accepted:
            try:
                # Получаем данные из формы
                guest_data = booking_dialog.form.get_data()
                
                # Получаем room_id через прямой запрос к API
                response = requests.get(
                    f"http://localhost:5000/api/rooms?room_number={room_number}",
                    timeout=5
                )
                response.raise_for_status()
                rooms = response.json()
                
                if not rooms or not isinstance(rooms, list) or len(rooms) == 0:
                    raise Exception("Не удалось получить информацию о номере")
                
                room_id = rooms[0].get("room_id")
                if not room_id:
                    raise Exception("Номер не найден в базе данных")

                # Формируем данные для отправки
                booking_data = {
                    "room_id": room_id,
                    "check_in_date": guest_data["check_in"],
                    "check_out_date": guest_data["check_out"],
                    "adults": booking_dialog.adults_spin.value(),
                    "children": booking_dialog.children_spin.value(),
                    "guest": {
                        "passport_number": guest_data["passport_number"],
                        "first_name": guest_data["first_name"],
                        "last_name": guest_data["last_name"],
                        "phone": guest_data["phone"],
                        "email": guest_data.get("email"),
                        "address": None
                    },
                    "payment_method": booking_dialog.payment_map.get(
                        booking_dialog.payment_combo.currentText(),
                        "cash"  # значение по умолчанию
                    ),
                    "services": [
                        {
                            "service_id": int(service["service_id"]),
                            "quantity": int(service["quantity"])
                        }
                        for service in booking_dialog.get_selected_services()
                        if service["quantity"] > 0
                    ]
                }

                # Логирование для отладки
                print("Отправляемые данные на сервер:")
                import pprint
                pprint.pprint(booking_data)

                # Отправка запроса
                response = requests.post(
                    "http://localhost:5000/api/bookings",
                    json=booking_data,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                # Проверка ответа
                if response.status_code != 201:
                    error_msg = response.json().get("error", "Неизвестная ошибка сервера")
                    raise Exception(f"Ошибка сервера: {error_msg}")

                QtWidgets.QMessageBox.information(
                    self.main_window,
                    "Успех",
                    f"Номер {room_number} успешно забронирован!"
                )
                self.fetch_rooms_data()  # Обновляем список номеров

            except requests.exceptions.RequestException as e:
                QtWidgets.QMessageBox.critical(
                    self.main_window,
                    "Ошибка сети",
                    f"Ошибка соединения с сервером:\n{str(e)}"
                )
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self.main_window,
                    "Ошибка бронирования",
                    f"Произошла ошибка:\n{str(e)}\n\nПроверьте данные и повторите попытку."
                )
                print("Подробности ошибки:", traceback.format_exc())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")  # Установка стиля Fusion
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())