from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
    QWidget, QScrollArea, QComboBox, QDateEdit, QMessageBox, QApplication
)
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtCore import Qt, QDate, QTimer


class GuestForm(QWidget):
    def __init__(self, index, removable=False):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        font = QFont("Arial", 20)
        style_common = """
            QLineEdit, QComboBox, QDateEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 6px 10px;
                font-size: 20px;
                max-width: 600px;
                min-width: 600px;
            }
        """

        title_layout = QHBoxLayout()
        title = QLabel(f"Постоялец {index + 1}")
        title.setStyleSheet("font-weight: bold; font-size: 35px;")
        title_layout.addWidget(title, alignment=Qt.AlignLeft)
        layout.addLayout(title_layout)

        layout.addWidget(QLabel("Фамилия"))
        self.surname = QLineEdit()
        self.surname.setPlaceholderText("Введите фамилию")
        self.surname.setFont(font)
        self.surname.setStyleSheet(style_common)
        layout.addWidget(self.surname, alignment=Qt.AlignCenter)

        layout.addWidget(QLabel("Имя"))
        self.name = QLineEdit()
        self.name.setPlaceholderText("Введите имя")
        self.name.setFont(font)
        self.name.setStyleSheet(style_common)
        layout.addWidget(self.name, alignment=Qt.AlignCenter)

        layout.addWidget(QLabel("Отчество"))
        self.patronymic = QLineEdit()
        self.patronymic.setPlaceholderText("Введите отчество(при наличии)")
        self.patronymic.setFont(font)
        self.patronymic.setStyleSheet(style_common)
        layout.addWidget(self.patronymic, alignment=Qt.AlignCenter)

        layout.addWidget(QLabel("Паспорт"))
        self.passport = QLineEdit()
        self.passport.setPlaceholderText("Введите номер паспорта")
        self.passport.setValidator(QIntValidator())
        self.passport.setFont(font)
        self.passport.setStyleSheet(style_common)
        layout.addWidget(self.passport, alignment=Qt.AlignCenter)

        layout.addWidget(QLabel("Телефон"))
        self.phone = QLineEdit()
        self.phone.setPlaceholderText("Введите номер телефона в формате 8**********")
        self.phone.setFont(font)
        self.phone.setStyleSheet(style_common)
        layout.addWidget(self.phone, alignment=Qt.AlignCenter)

        layout.addWidget(QLabel("Дата заезда"))
        self.checkin = QDateEdit()
        self.checkin.setDisplayFormat("dd.MM.yyyy")
        self.checkin.setCalendarPopup(True)
        self.checkin.setDate(QDate.currentDate())
        self.checkin.setFont(font)
        self.checkin.setStyleSheet(style_common)
        self.checkin.mousePressEvent = self.open_checkin_calendar
        layout.addWidget(self.checkin, alignment=Qt.AlignCenter)

        layout.addWidget(QLabel("Дата выезда"))
        self.checkout = QDateEdit()
        self.checkout.setDisplayFormat("dd.MM.yyyy")
        self.checkout.setCalendarPopup(True)
        self.checkout.setDate(QDate.currentDate())
        self.checkout.setFont(font)
        self.checkout.setStyleSheet(style_common)
        self.checkout.mousePressEvent = self.open_checkout_calendar
        layout.addWidget(self.checkout, alignment=Qt.AlignCenter)

        self.checkin.dateChanged.connect(self.update_checkout_min_date)
        self.update_checkout_min_date(self.checkin.date())

        layout.addWidget(QLabel("Питание"))
        self.food = QComboBox()
        self.food.addItems(["Да", "Нет"])
        self.food.setFont(font)
        self.food.setStyleSheet(style_common)
        layout.addWidget(self.food, alignment=Qt.AlignCenter)

        self.setLayout(layout)

        self.disable_wheel_events(self.checkin)
        self.disable_wheel_events(self.checkout)
        self.disable_wheel_events(self.food)

    def open_checkin_calendar(self, event):
        self.checkin.setFocus()
        self.checkin.calendarWidget().show()
        QDateEdit.mousePressEvent(self.checkin, event)

    def open_checkout_calendar(self, event):
        self.checkout.setFocus()
        self.checkout.calendarWidget().show()
        QDateEdit.mousePressEvent(self.checkout, event)

    def update_checkout_min_date(self, date):
        self.checkout.setMinimumDate(date)

    def is_valid(self):
        return self.checkout.date() > self.checkin.date()

    def disable_wheel_events(self, widget):
        def block_wheel(event):
            event.ignore()
        widget.wheelEvent = block_wheel


class GuestBookingDialog(QDialog):
    def __init__(self, max_guests=3):
        super().__init__()
        self.setWindowTitle("Заселение гостей")
        self.resize(1200, 800)
        self.setMinimumWidth(600)
        self.showMaximized()

        self.max_guests = max_guests
        self.forms = []

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.form_layout = QVBoxLayout(self.scroll_widget)
        self.form_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.scroll_area.setWidget(self.scroll_widget)
        self.main_layout.addWidget(self.scroll_area)

        self.button_layout = QHBoxLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)

        self.add_guest_button = QPushButton("Add")
        self.add_guest_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #007BFF;
                border: 2px solid #007BFF;
                border-radius: 10px;
                font-size: 24px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #e6f0ff;
            }
        """)
        self.add_guest_button.clicked.connect(self.add_guest_form)
        self.button_layout.addWidget(self.add_guest_button)

        self.remove_guest_button = QPushButton("Delete")
        self.remove_guest_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: red;
                border: 2px solid red;
                border-radius: 10px;
                font-size: 24px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #ffe6e6;
            }
        """)
        self.remove_guest_button.clicked.connect(self.remove_last_guest_form)
        self.button_layout.addWidget(self.remove_guest_button)

        self.main_layout.addLayout(self.button_layout)

        self.confirm_button = QPushButton("Подтвердить")
        self.confirm_button.setStyleSheet(
            "background-color: #007BFF; color: white; padding: 10px; border-radius: 5px; font-size: 16px;"
        )
        self.confirm_button.clicked.connect(self.confirm_data)
        self.main_layout.addWidget(self.confirm_button, alignment=Qt.AlignCenter)

        self.add_guest_form(removable=False)
        self.update_remove_button_state()

    def add_guest_form(self, removable=True):
        if len(self.forms) >= self.max_guests:
            return
        form = GuestForm(len(self.forms), removable=removable)
        self.forms.append(form)
        self.form_layout.addWidget(form)
        self.update_remove_button_state()
        QTimer.singleShot(250, lambda: self.scroll_area.ensureWidgetVisible(form))

    def remove_last_guest_form(self):
        if len(self.forms) <= 1:
            return
        form = self.forms.pop()
        self.form_layout.removeWidget(form)
        form.deleteLater()
        self.rename_guests()
        self.update_remove_button_state()

    def rename_guests(self):
        for i, f in enumerate(self.forms):
            f.layout().itemAt(0).layout().itemAt(0).widget().setText(f"Постоялец {i + 1}")

    def update_remove_button_state(self):
        self.remove_guest_button.setEnabled(len(self.forms) > 1)
    #проверка на корректное заполнение
    def confirm_data(self):
        for i, form in enumerate(self.forms):
            if not form.surname.text().strip():
                QMessageBox.warning(self, "Ошибка", f"У постояльца {i + 1} не заполнено поле 'Фамилия'.")
                return
            if not form.name.text().strip():
                QMessageBox.warning(self, "Ошибка", f"У постояльца {i + 1} не заполнено поле 'Имя'.")
                return
            if not form.passport.text().strip():
                QMessageBox.warning(self, "Ошибка", f"У постояльца {i + 1} не заполнено поле 'Паспорт'.")
                return
            if not form.phone.text().strip():
                QMessageBox.warning(self, "Ошибка", f"У постояльца {i + 1} не заполнено поле 'Телефон'.")
                return

            if not form.is_valid():
                QMessageBox.warning(self, "Ошибка",
                                    f"Дата выезда у постояльца #{i + 1} не может быть раньше или равна дате заезда.")
                return

        print("Подтверждены данные:")
        for i, form in enumerate(self.forms):
            print(f"Постоялец #{i + 1}:", self.get_guest_data()[i])

        result = QMessageBox.information(self, "Успешно", "Данные успешно подтверждены!")
        if result == QMessageBox.Ok:
            self.accept()  # Закрытие окна

    def get_guest_data(self):
        data = []
        for form in self.forms:
            data.append({
                "Фамилия": form.surname.text(),
                "Имя": form.name.text(),
                "Отчество": form.patronymic.text(),
                "Паспорт": form.passport.text(),
                "Телефон": form.phone.text(),
                "Дата заезда": form.checkin.date().toString("dd.MM.yyyy"),
                "Дата выезда": form.checkout.date().toString("dd.MM.yyyy"),
                "Питание": form.food.currentText(),
            })
        return data


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = GuestBookingDialog(max_guests=3)
    dialog.exec_()
