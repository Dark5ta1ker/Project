from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 500)
        MainWindow.setFixedSize(450, 500)
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        MainWindow.setStyleSheet("background-color: white;")  # фон белый
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Основной layout для центрирования содержимого
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addStretch()  # сверху

        # Внутренний виджет
        self.widget = QtWidgets.QWidget(self.centralwidget)


        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout.setContentsMargins(25, 25, 25, 25)
        self.verticalLayout.setObjectName("verticalLayout")
        main_layout.addWidget(self.widget, alignment=QtCore.Qt.AlignHCenter)
        main_layout.addStretch()  # снизу

        # Название окна
        self.name_input = QtWidgets.QLabel(self.widget)
        self.name_input.setStyleSheet("""
            color: #0C5FFF;
            font: bold 16pt "Arial";
        """)
        self.name_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.name_input.setFixedSize(250, 110)
        self.name_input.setTextFormat(QtCore.Qt.AutoText)
        self.name_input.setAlignment(QtCore.Qt.AlignCenter)
        self.name_input.setWordWrap(True)
        self.name_input.setObjectName("name_input")
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.name_input, alignment=QtCore.Qt.AlignHCenter)

        # Подпись логина
        self.log_text_label = QtWidgets.QLabel(self.widget)
        self.log_text_label.setStyleSheet("""
            color: #333333;
            font: 11pt "Arial";
        """)
        self.log_text_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.log_text_label.setFixedSize(250, 25)
        self.log_text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.log_text_label.setObjectName("log_text_label")
        self.verticalLayout.addWidget(self.log_text_label, alignment=QtCore.Qt.AlignHCenter)

        # Поле логина
        self.log_input = QtWidgets.QLineEdit(self.widget)
        self.log_input.setAlignment(QtCore.Qt.AlignCenter)
        self.log_input.setStyleSheet("""
            font: 10pt "Arial";
            background-color: #F5F5F5;
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            padding: 5px;
        """)
        self.log_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.log_input.setFixedSize(250, 30)
        self.log_input.setObjectName("log_input")
        self.verticalLayout.addWidget(self.log_input, alignment=QtCore.Qt.AlignHCenter)

        # Подпись пароля
        self.pass_text_label = QtWidgets.QLabel(self.widget)
        self.pass_text_label.setStyleSheet("""
            color: #333333;
            font: 11pt "Arial";
        """)
        self.pass_text_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.pass_text_label.setFixedSize(250, 25)
        self.pass_text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pass_text_label.setObjectName("pass_text_label")
        self.verticalLayout.addWidget(self.pass_text_label, alignment=QtCore.Qt.AlignHCenter)

        # Поле пароля
        self.pass_input = QtWidgets.QLineEdit(self.widget)
        self.pass_input.setAlignment(QtCore.Qt.AlignCenter)
        self.pass_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_input.setStyleSheet("""
            font: 10pt "Arial";
            background-color: #F5F5F5;
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            padding: 5px;
        """)
        self.pass_input.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.pass_input.setFixedSize(250, 30)
        self.pass_input.setObjectName("pass_input")
        self.verticalLayout.addWidget(self.pass_input, alignment=QtCore.Qt.AlignHCenter)

        self.verticalLayout.addStretch()

        # Кнопка входа
        self.input_but = QtWidgets.QPushButton(self.widget)
        self.input_but.setStyleSheet("""
            background-color: #0C5FFF;
            color: white;
            font: bold 12pt "Arial";
            border: none;
            border-radius: 6px;
            padding: 8px 0;
        """)
        self.input_but.setFixedSize(120, 40)
        self.input_but.setObjectName("input_but")
        #выравнивание сраной кнопки:
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.input_but)
        button_layout.addStretch()
        self.verticalLayout.addLayout(button_layout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Авторизация"))
        self.name_input.setText(_translate("MainWindow", "Вход в систему управления отелем"))
        self.log_text_label.setText(_translate("MainWindow", "Введите логин"))
        self.pass_text_label.setText(_translate("MainWindow", "Введите пароль"))
        self.input_but.setText(_translate("MainWindow", "Войти"))