from PyQt5 import QtCore, QtGui, QtWidgets
import requests
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 720)  # Уменьшен размер по умолчанию
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: white;")
        self.centralwidget.setObjectName("centralwidget")

        # Основная вертикальная компоновка
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Заголовок
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setStyleSheet("""
            background-color: #0C5FFF;
            color: white;
            font: bold 16pt 'Arial';
        """)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("Система управления отелем")
        self.label.setFixedHeight(60)  # Фиксированная высота заголовка
        main_layout.addWidget(self.label)

        # Табы
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("""
            font: bold 12pt 'Arial';
            background-color: rgb(255, 255, 255);
            border-color: rgb(255, 85, 127);
        """)
        self.tabWidget.setObjectName("tabWidget")
        main_layout.addWidget(self.tabWidget)

        # Вкладка "Номера"
        self.rooms = QtWidgets.QWidget()
        self.setup_rooms_tab(self.rooms)
        self.tabWidget.addTab(self.rooms, "Номера")

        # Вкладка "Обслуживание"
        self.service = QtWidgets.QWidget()
        self.setup_service_tab(self.service)
        self.tabWidget.addTab(self.service, "Обслуживание")

        MainWindow.setCentralWidget(self.centralwidget)

    def setup_rooms_tab(self, tab):
        """Настройка вкладки 'Номера'."""
        layout = QtWidgets.QVBoxLayout(tab)

        # Фильтры
        filter_layout = QtWidgets.QGridLayout()
        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItems(["свободен", "занят", "обслуживание"])
        self.guests_combo = QtWidgets.QComboBox()
        self.guests_combo.addItems(["1", "2", "3"])
        self.check_in_date = QtWidgets.QDateEdit(calendarPopup=True)
        self.check_out_date = QtWidgets.QDateEdit(calendarPopup=True)
        self.search_button = QtWidgets.QPushButton("Найти")

        # Стили для фильтров
        common_input_style = """
            QComboBox, QDateEdit {
                background-color: white;
                border: 1px solid #D9D9D9;
                padding: 4px;
                font: 10pt 'Arial';
            }
        """
        calendar_style = """
            QCalendarWidget {
                background-color: white;
                border: 1px solid #D9D9D9;
                font: 10pt 'Arial';
                color: black;
            }
            QCalendarWidget QToolButton {
                background-color: white;
                color: black;
                font: bold 10pt 'Arial';
                border: none;
                margin: 4px;
            }
            QCalendarWidget QAbstractItemView {
                background-color: white;
                selection-background-color: #0C5FFF;
                selection-color: white;
                gridline-color: #D9D9D9;
            }
        """

        self.status_combo.setStyleSheet(common_input_style)
        self.guests_combo.setStyleSheet(common_input_style)
        self.check_in_date.setStyleSheet(common_input_style)
        self.check_out_date.setStyleSheet(common_input_style)
        self.check_in_date.setCalendarPopup(True)
        self.check_out_date.setCalendarPopup(True)
        self.check_in_date.calendarWidget().setStyleSheet(calendar_style)
        self.check_out_date.calendarWidget().setStyleSheet(calendar_style)

        filter_layout.addWidget(QtWidgets.QLabel("Статус"), 0, 0)
        filter_layout.addWidget(self.status_combo, 1, 0)
        filter_layout.addWidget(QtWidgets.QLabel("Число гостей"), 0, 1)
        filter_layout.addWidget(self.guests_combo, 1, 1)
        filter_layout.addWidget(QtWidgets.QLabel("Дата заезда"), 0, 2)
        filter_layout.addWidget(self.check_in_date, 1, 2)
        filter_layout.addWidget(QtWidgets.QLabel("Дата выезда"), 0, 3)
        filter_layout.addWidget(self.check_out_date, 1, 3)
        filter_layout.addWidget(self.search_button, 1, 4)

        layout.addLayout(filter_layout)

        # Таблица для отображения номеров
        self.tableView = QtWidgets.QTableView(tab)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.tableView)

        # Подключение кнопки "Найти"
        self.search_button.clicked.connect(self.fetch_rooms_data)

    def setup_service_tab(self, tab):
        """Настройка вкладки 'Обслуживание'."""
        layout = QtWidgets.QVBoxLayout(tab)

        # Таблица для отображения данных об обслуживании
        self.tableView_2 = QtWidgets.QTableView(tab)
        self.tableView_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView_2.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.tableView_2.horizontalHeader().setStretchLastSection(True)
        self.tableView_2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableView_2.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(self.tableView_2)

    def fetch_rooms_data(self):
        """Получение данных о номерах с бэкенда."""
        try:
            # Параметры фильтрации
            status = self.status_combo.currentText()
            guests = self.guests_combo.currentText()
            check_in = self.check_in_date.date().toString("yyyy-MM-dd")
            check_out = self.check_out_date.date().toString("yyyy-MM-dd")

            # Отправка GET-запроса к бэкенду
            response = requests.get(
                "http://localhost:5000/api/rooms",
                params={
                    "status": status,
                    "guests": guests,
                    "check_in": check_in,
                    "check_out": check_out,
                }
            )
            response.raise_for_status()  # Проверка на ошибки HTTP

            # Обработка данных
            rooms_data = response.json()

            # Создание модели для таблицы
            model = QtGui.QStandardItemModel()
            model.setHorizontalHeaderLabels(["ID", "Номер", "Тип", "Доступность"])

            for room in rooms_data:
                row = [
                    QtGui.QStandardItem(str(room["id"])),
                    QtGui.QStandardItem(room["number"]),
                    QtGui.QStandardItem(room["type"]),
                    QtGui.QStandardItem("Да" if room["available"] else "Нет"),
                ]
                model.appendRow(row)

            self.tableView.setModel(model)

        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(self.centralwidget, "Ошибка", f"Не удалось получить данные: {e}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())