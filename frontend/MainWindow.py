from PyQt5 import QtCore, QtGui, QtWidgets
from room_info_window import RoomInfoWindow
import requests
import traceback

class TableItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Настройка вертикального градиента для всей строки
        gradient = QtGui.QLinearGradient(option.rect.topLeft(), option.rect.bottomLeft())
        gradient.setColorAt(0, QtGui.QColor(240, 240, 240))  # Слегка темнее сверху
        gradient.setColorAt(0.5, QtGui.QColor(250, 250, 250))  # Светлее в центре
        gradient.setColorAt(1, QtGui.QColor(240, 240, 240))  # Слегка темнее снизу
        
        # Если строка выделена - используем синий градиент
        if option.state & QtWidgets.QStyle.State_Selected:
            gradient = QtGui.QLinearGradient(option.rect.topLeft(), option.rect.bottomLeft())
            gradient.setColorAt(0, QtGui.QColor(10, 80, 200))
            gradient.setColorAt(1, QtGui.QColor(5, 60, 180))
        
        painter.fillRect(option.rect, gradient)
        
        # Рисуем текст (всегда по центру)
        painter.save()
        text_color = QtCore.Qt.white if option.state & QtWidgets.QStyle.State_Selected else QtCore.Qt.black
        painter.setPen(text_color)
        
        text = index.data(QtCore.Qt.DisplayRole)
        if text is not None:
            painter.drawText(
                option.rect, 
                QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter, 
                str(text)
            )
        painter.restore()

    def sizeHint(self, option, index):
        size = super().sizeHint(option, index)
        size.setHeight(40)  # Фиксированная высота строки
        return size

    def createEditor(self, parent, option, index):
        return None  # Запрещаем редактирование

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

        # Создаем и настраиваем таблицу до подключения сигналов
        self.setup_rooms_tab()
        main_layout.addWidget(self.tabWidget)

        # Создаем нижнюю панель после таблицы
        self.setup_bottom_panel()
        main_layout.addWidget(self.bottom_panel)
        
        MainWindow.setCentralWidget(self.centralwidget)

        # Подключаем сигналы после полной инициализации
        self.connect_signals()

    def setup_rooms_tab(self):
        """Настройка вкладки с номерами"""
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

        self.rooms_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(self.rooms_tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Панель фильтров
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

        # Таблица номеров
        self.rooms_table = QtWidgets.QTableView()
        self.rooms_table.setObjectName("roomsTable")
        self.rooms_table.setStyleSheet("""
            QTableView {
                font: 11pt 'Arial';
                gridline-color: transparent;
                border: none;
                background-color: transparent;
                selection-background-color: transparent;
            }
            QHeaderView::section {
                background-color: #0C5FFF;
                color: white;
                padding: 12px;
                font: bold 11pt 'Arial';
                border: none;
            }
        """)
        
        # Настройка поведения таблицы
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

        # Вкладка обслуживания
        self.service_tab = QtWidgets.QWidget()
        service_layout = QtWidgets.QVBoxLayout(self.service_tab)
        service_layout.setContentsMargins(10, 10, 10, 10)
        
        self.service_table = QtWidgets.QTableView()
        self.service_table.setStyleSheet("""
            QTableView {
                font: 11pt 'Arial';
                gridline-color: transparent;
                border: none;
                background-color: #f9f9f9;
                alternate-background-color: #f0f0f0;
                selection-background-color: #0C5FFF;
                selection-color: white;
            }
            QTableView::item {
                border: none;
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #0C5FFF;
                color: white;
                padding: 12px;
                font: bold 11pt 'Arial';
                border: none;
            }
        """)
        
        service_layout.addWidget(self.service_table)
        self.tabWidget.addTab(self.service_tab, "Обслуживание")

    def setup_bottom_panel(self):
        """Настройка нижней панели с кнопками"""
        self.bottom_panel = QtWidgets.QFrame()
        self.bottom_panel.setStyleSheet("background-color: #f0f0f0; border-top: 1px solid #ddd;")
        bottom_layout = QtWidgets.QHBoxLayout(self.bottom_panel)
        bottom_layout.setContentsMargins(10, 5, 10, 5)
        
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
        bottom_layout.addWidget(self.info_button)
        bottom_layout.addStretch()

    def connect_signals(self):
        """Подключаем сигналы после полной инициализации"""
        self.info_button.clicked.connect(self.show_room_info)
        if self.rooms_table.selectionModel():
            self.rooms_table.selectionModel().selectionChanged.connect(self.on_room_selected)
        else:
            print("Warning: Selection model not available")

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

    def on_room_selected(self, selected, deselected):
        """Обработчик выбора строки в таблице"""
        self.info_button.setEnabled(len(selected.indexes()) > 0)

    def show_room_info(self):
        """Показывает окно с полной информацией о номере"""
        selected = self.rooms_table.selectionModel().selectedRows()
        if not selected:
            return
        
        row = selected[0].row()
        room_number = self.rooms_table.model().index(row, 0).data()
        
        # Создаем и показываем окно информации
        self.info_window = RoomInfoWindow(room_number, self.main_window)
        self.info_window.exec_()

    def fetch_rooms_data(self):
        """Загрузка данных о номерах"""
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

            response = requests.get(
                "http://localhost:5000/ui/rooms",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            rooms_data = response.json()

            if not isinstance(rooms_data, list):
                raise ValueError("Ожидался список номеров")

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

                status_text = {
                    'available': 'Свободен',
                    'occupied': 'Занят',
                    'maintenance': 'На обслуживании'
                }.get(room['status'], 'Неизвестно')

                row = [
                    QtGui.QStandardItem(str(room['room_number'])),
                    QtGui.QStandardItem(type_map.get(room['type'], room['type'])),
                    QtGui.QStandardItem(str(room['capacity'])),
                    QtGui.QStandardItem(status_text),
                    QtGui.QStandardItem(f"{room['daily_rate']:,.2f} ₽".replace(",", " "))
                ]
                model.appendRow(row)

            self.rooms_table.setModel(model)

            # 🔥 ВАЖНО: подключаем сигнал выбора после назначения модели
            self.rooms_table.selectionModel().selectionChanged.connect(self.on_room_selected)

            if model.rowCount() == 0:
                QtWidgets.QMessageBox.information(
                    self.main_window,
                    "Результаты поиска",
                    "Номера по заданным критериям не найдены"
                )
            else:
                self.info_button.setEnabled(False)  # Сброс, пока ничего не выбрано

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