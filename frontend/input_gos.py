from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Настройка главного окна приложения
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 500)  # Установка размеров окна
        MainWindow.setFixedSize(450, 500)  # Фиксированный размер окна
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)  # Включение кнопок закрытия и сворачивания
        MainWindow.setStyleSheet("background-color: white;")  # Белый фон окна

        # Центральный виджет для размещения элементов интерфейса
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Основной layout для центрирования содержимого
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
        main_layout.addStretch()  # Добавляем пустое пространство сверху

        # Внутренний виджет для размещения элементов формы
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")

        # Вертикальный layout для внутреннего виджета
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignHCenter)  # Выравнивание по центру по горизонтали
        self.verticalLayout.setContentsMargins(25, 25, 25, 25)  # Отступы внутри виджета
        self.verticalLayout.setObjectName("verticalLayout")

        # Добавление внутреннего виджета в основной layout
        main_layout.addWidget(self.widget, alignment=QtCore.Qt.AlignHCenter)
        main_layout.addStretch()  # Добавляем пустое пространство снизу

        # Название окна (заголовок)
        self.name_input = QtWidgets.QLabel(self.widget)
        self.name_input.setStyleSheet("""
            color: #0C5FFF;  /* Синий цвет текста */
            font: bold 16pt "Arial";  /* Жирный шрифт Arial */
        """)
        self.name_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # Фиксированный размер
        self.name_input.setFixedSize(250, 110)  # Размер виджета
        self.name_input.setTextFormat(QtCore.Qt.AutoText)  # Автоматический формат текста
        self.name_input.setAlignment(QtCore.Qt.AlignCenter)  # Выравнивание текста по центру
        self.name_input.setWordWrap(True)  # Перенос текста на новую строку
        self.name_input.setObjectName("name_input")
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.name_input, alignment=QtCore.Qt.AlignHCenter)

        # Подпись для поля логина
        self.log_text_label = QtWidgets.QLabel(self.widget)
        self.log_text_label.setStyleSheet("""
            color: #333333;  /* Темно-серый цвет текста */
            font: 11pt "Arial";  /* Шрифт Arial */
        """)
        self.log_text_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # Фиксированный размер
        self.log_text_label.setFixedSize(250, 25)  # Размер виджета
        self.log_text_label.setAlignment(QtCore.Qt.AlignCenter)  # Выравнивание текста по центру
        self.log_text_label.setObjectName("log_text_label")
        self.verticalLayout.addWidget(self.log_text_label, alignment=QtCore.Qt.AlignHCenter)

        # Поле ввода логина
        self.log_input = QtWidgets.QLineEdit(self.widget)
        self.log_input.setAlignment(QtCore.Qt.AlignCenter)  # Выравнивание текста по центру
        self.log_input.setStyleSheet("""
            font: 10pt "Arial";  /* Шрифт Arial */
            background-color: #F5F5F5;  /* Светло-серый фон */
            border: 1px solid #CCCCCC;  /* Граница */
            border-radius: 6px;  /* Закругленные углы */
            padding: 5px;  /* Отступы внутри поля */
        """)
        self.log_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # Фиксированный размер
        self.log_input.setFixedSize(250, 30)  # Размер виджета
        self.log_input.setObjectName("log_input")
        self.verticalLayout.addWidget(self.log_input, alignment=QtCore.Qt.AlignHCenter)

        # Подпись для поля пароля
        self.pass_text_label = QtWidgets.QLabel(self.widget)
        self.pass_text_label.setStyleSheet("""
            color: #333333;  /* Темно-серый цвет текста */
            font: 11pt "Arial";  /* Шрифт Arial */
        """)
        self.pass_text_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # Фиксированный размер
        self.pass_text_label.setFixedSize(250, 25)  # Размер виджета
        self.pass_text_label.setAlignment(QtCore.Qt.AlignCenter)  # Выравнивание текста по центру
        self.pass_text_label.setObjectName("pass_text_label")
        self.verticalLayout.addWidget(self.pass_text_label, alignment=QtCore.Qt.AlignHCenter)

        # Поле ввода пароля
        self.pass_input = QtWidgets.QLineEdit(self.widget)
        self.pass_input.setAlignment(QtCore.Qt.AlignCenter)  # Выравнивание текста по центру
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.Password)  # Скрытие вводимых символов
        self.pass_input.setStyleSheet("""
            font: 10pt "Arial";  /* Шрифт Arial */
            background-color: #F5F5F5;  /* Светло-серый фон */
            border: 1px solid #CCCCCC;  /* Граница */
            border-radius: 6px;  /* Закругленные углы */
            padding: 5px;  /* Отступы внутри поля */
        """)
        self.pass_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)  # Фиксированный размер
        self.pass_input.setFixedSize(250, 30)  # Размер виджета
        self.pass_input.setObjectName("pass_input")
        self.verticalLayout.addWidget(self.pass_input, alignment=QtCore.Qt.AlignHCenter)

        self.verticalLayout.addStretch()

        # Кнопка входа
        self.input_but = QtWidgets.QPushButton(self.widget)
        self.input_but.setStyleSheet("""
            background-color: #0C5FFF;  /* Синий фон */
            color: white;  /* Белый текст */
            font: bold 12pt "Arial";  /* Жирный шрифт Arial */
            border: none;  /* Без границ */
            border-radius: 6px;  /* Закругленные углы */
            padding: 8px 0;  /* Отступы внутри кнопки */
        """)
        self.input_but.setFixedSize(120, 40)  # Размер кнопки
        self.input_but.setObjectName("input_but")

        # Выравнивание кнопки по центру
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()  # Пространство слева
        button_layout.addWidget(self.input_but)  # Кнопка
        button_layout.addStretch()  # Пространство справа
        self.verticalLayout.addLayout(button_layout)

        # Установка центрального виджета
        MainWindow.setCentralWidget(self.centralwidget)

        # Инициализация текстовых меток
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        # Локализация текстовых меток
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Авторизация"))  # Заголовок окна
        self.name_input.setText(_translate("MainWindow", "Вход в систему управления отелем"))  # Текст заголовка
        self.log_text_label.setText(_translate("MainWindow", "Введите логин"))  # Подпись для логина
        self.pass_text_label.setText(_translate("MainWindow", "Введите пароль"))  # Подпись для пароля
        self.input_but.setText(_translate("MainWindow", "Войти"))  # Текст на кнопке