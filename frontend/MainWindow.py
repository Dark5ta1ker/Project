from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import traceback

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.main_window = MainWindow

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)

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

        self.tabWidget = QtWidgets.QTabWidget()
        self.tabWidget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 5px;
                background: white;
            }
            QTabBar::tab {
                background: #e0e0e0;
                padding: 8px 15px;
                border: 1px solid #ddd;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
            }
        """)

        self.setup_rooms_tab()
        self.setup_service_tab()

        main_layout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

    def setup_rooms_tab(self):
        self.rooms_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.rooms_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        filter_panel = QtWidgets.QGroupBox("Фильтры поиска")
        filter_panel.setStyleSheet("""
            QGroupBox {
                font: bold 12pt 'Arial';
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)

        filter_layout = QtWidgets.QGridLayout()
        filter_layout.setContentsMargins(15, 20, 15, 15)
        filter_layout.setHorizontalSpacing(20)
        filter_layout.setVerticalSpacing(15)

        self.status_combo = self.create_combo_box(["Все", "Свободен", "Занят", "На обслуживании"])
        self.guests_combo = self.create_combo_box(["1", "2", "3", "4+"])

        self.check_in_date = self.create_date_edit()
        self.check_out_date = self.create_date_edit()
        self.check_out_date.setDate(QtCore.QDate.currentDate().addDays(1))

        self.search_button = QtWidgets.QPushButton("Поиск")
        self.search_button.setFixedHeight(40)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #0C5FFF;
                color: white;
                font: bold 12pt 'Arial';
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #084ED6;
            }
            QPushButton:pressed {
                background-color: #063AB2;
            }
        """)
        self.search_button.clicked.connect(self.fetch_rooms_data)

        filter_layout.addWidget(QtWidgets.QLabel("Статус номера:"), 0, 0)
        filter_layout.addWidget(self.status_combo, 1, 0)
        filter_layout.addWidget(QtWidgets.QLabel("Количество гостей:"), 0, 1)
        filter_layout.addWidget(self.guests_combo, 1, 1)
        filter_layout.addWidget(QtWidgets.QLabel("Дата заезда:"), 0, 2)
        filter_layout.addWidget(self.check_in_date, 1, 2)
        filter_layout.addWidget(QtWidgets.QLabel("Дата выезда:"), 0, 3)
        filter_layout.addWidget(self.check_out_date, 1, 3)
        filter_layout.addWidget(self.search_button, 1, 4, 1, 1)

        filter_panel.setLayout(filter_layout)
        layout.addWidget(filter_panel)

        self.rooms_table = QtWidgets.QTableView()
        self.rooms_table.setStyleSheet("""
            QTableView {
                font: 11pt 'Arial';
                gridline-color: #e0e0e0;
                selection-background-color: #0C5FFF;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #0C5FFF;
                color: white;
                padding: 8px;
                font: bold 11pt 'Arial';
                border: none;
            }
        """)
        self.rooms_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.rooms_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.rooms_table.verticalHeader().setDefaultSectionSize(40)
        layout.addWidget(self.rooms_table)

        self.tabWidget.addTab(self.rooms_tab, "Номера")

    def setup_service_tab(self):
        self.service_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.service_tab)
        layout.setContentsMargins(10, 10, 10, 10)

        self.service_table = QtWidgets.QTableView()
        layout.addWidget(self.service_table)

        self.tabWidget.addTab(self.service_tab, "Обслуживание")

    def create_combo_box(self, items):
        combo = QtWidgets.QComboBox()
        combo.addItems(items)
        combo.setStyleSheet("""
            QComboBox {
                font: 11pt 'Arial';
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QComboBox::drop-down {
                width: 30px;
                border-left: 1px solid #ddd;
            }
        """)
        combo.setFixedHeight(35)
        return combo

    def create_date_edit(self):
        date_edit = QtWidgets.QDateEdit(calendarPopup=True)
        date_edit.setDate(QtCore.QDate.currentDate())
        date_edit.setDisplayFormat("dd.MM.yyyy")
        date_edit.setStyleSheet("""
            QDateEdit {
                font: 11pt 'Arial';
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QCalendarWidget QToolButton {
                font: bold 10pt 'Arial';
            }
        """)
        date_edit.setFixedHeight(35)
        return date_edit

    def fetch_rooms_data(self):
        try:
            check_in = self.check_in_date.date()
            check_out = self.check_out_date.date()

            if check_out <= check_in:
                QtWidgets.QMessageBox.warning(
                    self.main_window,
                    "Ошибка дат",
                    "Дата выезда должна быть позже даты заезда"
                )
                return

            params = {
                "check_in": check_in.toString("yyyy-MM-dd"),
                "check_out": check_out.toString("yyyy-MM-dd")
            }

            status = self.status_combo.currentText()
            if status != "Все":
                status_map = {
                    "Свободен": "available",
                    "Занят": "occupied",
                    "На обслуживании": "maintenance"
                }
                params["status"] = status_map.get(status)

            guests = self.guests_combo.currentText()
            if guests == "4+":
                params["min_capacity"] = 4
            else:
                params["capacity"] = guests

            response = requests.get("http://localhost:5000/ui/rooms", params=params, timeout=10)
            response.raise_for_status()
            rooms_data = response.json()

            if not isinstance(rooms_data, list):
                raise ValueError("Ожидался список номеров")

            model = QtGui.QStandardItemModel()
            model.setHorizontalHeaderLabels(["Номер", "Тип", "Вместимость", "Статус", "Цена за сутки"])

            type_translations = {
                "Basic": "Базовый",
                "Advanced": "Комфорт",
                "Business": "Бизнес",
                "Dorm": "Общий"
            }

            for room in rooms_data:
                if not all(k in room for k in ['room_number', 'type', 'capacity', 'status', 'daily_rate']):
                    continue

                status_text = {
                    'available': 'Свободен',
                    'occupied': 'Занят',
                    'maintenance': 'На обслуживании'
                }.get(room['status'], 'Неизвестно')

                translated_type = type_translations.get(room['type'], room['type'])

                row = [
                    QtGui.QStandardItem(str(room['room_number'])),
                    QtGui.QStandardItem(translated_type),
                    QtGui.QStandardItem(str(room['capacity'])),
                    QtGui.QStandardItem(status_text),
                    QtGui.QStandardItem(f"{room['daily_rate']:,.2f} ₽".replace(",", " "))
                ]
                model.appendRow(row)

            self.rooms_table.setModel(model)

            if model.rowCount() == 0:
                QtWidgets.QMessageBox.information(
                    self.main_window,
                    "Результаты поиска",
                    "Номера по заданным критериям не найдены"
                )

        except requests.exceptions.RequestException as e:
            QtWidgets.QMessageBox.critical(
                self.main_window,
                "Ошибка соединения",
                f"Ошибка при запросе данных:\n{str(e)}"
            )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.main_window,
                "Ошибка",
                f"Непредвиденная ошибка:\n{str(e)}"
            )

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
