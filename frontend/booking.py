from PyQt5 import QtWidgets, QtCore, QtGui
import requests

class GuestForm(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.booking_dialog = None  # Ссылка на родительский диалог
        layout = QtWidgets.QFormLayout()
        layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        layout.setFormAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        font = QtGui.QFont("Arial", 11)

        self.surname = QtWidgets.QLineEdit()
        self.name = QtWidgets.QLineEdit()
        self.patronymic = QtWidgets.QLineEdit()
        self.passport = QtWidgets.QLineEdit()
        self.email = QtWidgets.QLineEdit()
        self.phone = QtWidgets.QLineEdit()

        for widget in [self.surname, self.name, self.patronymic, self.passport, self.email, self.phone]:
            widget.setFont(font)
            widget.setFixedHeight(30)
            widget.setStyleSheet("""
                QLineEdit {
                    padding: 5px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    background: white;
                }
            """)

        label_style = "font: 11pt 'Arial'; color: #333;"
        layout.addRow(self.create_label("Фамилия*", label_style), self.surname)
        layout.addRow(self.create_label("Имя*", label_style), self.name)
        layout.addRow(self.create_label("Отчество", label_style), self.patronymic)
        layout.addRow(self.create_label("Паспорт*", label_style), self.passport)
        layout.addRow(self.create_label("Email", label_style), self.email)
        layout.addRow(self.create_label("Телефон", label_style), self.phone)

        self.setLayout(layout)

    def create_label(self, text, style):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet(style)
        return label

    def is_valid(self):
        return all([
            self.surname.text().strip(),
            self.name.text().strip(),
            self.passport.text().strip()
        ])

    def get_data(self):
        if not self.booking_dialog:
            raise RuntimeError("BookingDialog reference not set")

        return {
            "passport_number": self.passport.text().strip(),
            "first_name": self.name.text().strip(),
            "last_name": self.surname.text().strip(),
            "email": self.email.text().strip() or None,
            "phone": self.phone.text().strip(),
            "address": None,
            "check_in": self.booking_dialog.checkin.date().toString("yyyy-MM-dd"),
            "check_out": self.booking_dialog.checkout.date().toString("yyyy-MM-dd")
        }

class GuestBookingDialog(QtWidgets.QDialog):
    def __init__(self, room_number, room_capacity):
        super().__init__()
        self.setWindowTitle(f"Бронирование | Номер {room_number}")
        self.setMinimumSize(900, 700)
        self.room_number = room_number
        self.room_capacity = room_capacity

        self.setStyleSheet("QDialog { background-color: #f5f5f5; }")

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.header = QtWidgets.QLabel(f"Номер: {room_number} | Вместимость: {room_capacity}")
        self.header.setStyleSheet("""
            QLabel {
                background-color: #0C5FFF;
                color: white;
                font: bold 16pt 'Arial';
                padding: 10px;
                border-radius: 6px;
            }
        """)
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.header)

        # Блок дат
        date_layout = QtWidgets.QHBoxLayout()
        self.checkin = self.create_date_edit()
        self.checkout = self.create_date_edit(QtCore.QDate.currentDate().addDays(1))

        self.checkin.dateChanged.connect(self.update_checkout_min_date)
        self.update_checkout_min_date(self.checkin.date())

        label_style = "font: 11pt 'Arial'; color: #333;"
        date_layout.addWidget(self.create_label("Дата заезда:", label_style))
        date_layout.addWidget(self.checkin)
        date_layout.addSpacing(20)
        date_layout.addWidget(self.create_label("Дата выезда:", label_style))
        date_layout.addWidget(self.checkout)
        layout.addLayout(date_layout)

        # Взрослые и дети
        guest_count_layout = QtWidgets.QHBoxLayout()
        guest_count_layout.addWidget(self.create_label("Взрослые:", label_style))
        self.adults_spin = QtWidgets.QSpinBox()
        self.adults_spin.setMinimum(1)
        self.adults_spin.setMaximum(room_capacity)
        guest_count_layout.addWidget(self.adults_spin)

        guest_count_layout.addWidget(self.create_label("Дети:", label_style))
        self.children_spin = QtWidgets.QSpinBox()
        self.children_spin.setMaximum(room_capacity)
        guest_count_layout.addWidget(self.children_spin)
        layout.addLayout(guest_count_layout)

        # Форма гостя
        self.form = GuestForm()
        self.form.booking_dialog = self  # Явная передача ссылки
        
        form_box = QtWidgets.QGroupBox("Данные гостя")
        form_layout = QtWidgets.QVBoxLayout(form_box)
        form_layout.addWidget(self.form)
        form_box.setStyleSheet("""
            QGroupBox {
                font: bold 12pt 'Arial';
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        layout.addWidget(form_box)

        # Примечание
        hint = QtWidgets.QLabel("Поля, помеченные * обязательны для заполнения")
        hint.setStyleSheet("color: #666; font: 10pt 'Arial';")
        layout.addWidget(hint)

        # Способ оплаты
        self.payment_combo = QtWidgets.QComboBox()
        self.payment_map = {
            "Наличные": "cash",
            "Карта": "credit_card",
            "Банковский перевод": "bank_transfer",
            "Онлайн": "online"
        }
        self.payment_combo.addItems(self.payment_map.keys())
        self.payment_combo.setFixedHeight(30)
        self.payment_combo.setStyleSheet("""
            QComboBox {
                font: 11pt 'Arial';
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background: white;
            }
        """)
        layout.addWidget(self.create_label("Способ оплаты:", label_style))
        layout.addWidget(self.payment_combo)

        # Услуги
        self.services_group = QtWidgets.QGroupBox("Дополнительные услуги")
        self.services_layout = QtWidgets.QFormLayout()
        self.services_group.setLayout(self.services_layout)
        self.service_inputs = {}
        layout.addWidget(self.services_group)
        self.load_services()

        # Подтверждение
        self.confirm_btn = QtWidgets.QPushButton("Подтвердить бронирование")
        self.confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font: bold 12pt 'Arial';
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover { background-color: #45a049; }
            QPushButton:pressed { background-color: #3e8e41; }
        """)
        self.confirm_btn.clicked.connect(self.confirm_booking)
        layout.addWidget(self.confirm_btn, alignment=QtCore.Qt.AlignCenter)

    def create_label(self, text, style):
        label = QtWidgets.QLabel(text)
        label.setStyleSheet(style)
        return label

    def create_date_edit(self, date=QtCore.QDate.currentDate()):
        de = QtWidgets.QDateEdit()
        de.setDate(date)
        de.setCalendarPopup(True)
        de.setDisplayFormat("dd.MM.yyyy")
        de.setStyleSheet("""
            QDateEdit {
                font: 11pt 'Arial';
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background: white;
            }
        """)
        de.setFixedHeight(32)
        return de

    def update_checkout_min_date(self, date):
        self.checkout.setMinimumDate(date.addDays(1))

    def load_services(self):
        try:
            response = requests.get("http://localhost:5000/api/services")
            services = response.json()
            for s in services:
                spin = QtWidgets.QSpinBox()
                spin.setRange(0, 10)
                self.services_layout.addRow(f"{s['name']} ({s['price']} ₽)", spin)
                self.service_inputs[s["service_id"]] = spin
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", str(e))

    def confirm_booking(self):
        if not self.form.is_valid():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля гостя.")
            return
        if self.checkout.date() <= self.checkin.date():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Дата выезда должна быть позже даты заезда.")
            return

        booking_data = {
            "room_number": self.room_number,
            "guest": self.form.get_data(),  # Используем form.get_data() вместо get_guest_data()
            "dates": {
                "check_in": self.checkin.date().toString("yyyy-MM-dd"),
                "check_out": self.checkout.date().toString("yyyy-MM-dd")
            },
            "guests": {
                "adults": self.adults_spin.value(),
                "children": self.children_spin.value()
            },
            "payment": self.payment_map[self.payment_combo.currentText()],
            "services": self.get_selected_services()
        }

        # Здесь можно добавить отправку данных на сервер
        print("Бронирование:", booking_data)  # Для отладки
        
        QtWidgets.QMessageBox.information(self, "Успех", "Бронирование подтверждено!")
        self.accept()

    def get_selected_services(self):
        return [{"service_id": sid, "quantity": spin.value()}
                for sid, spin in self.service_inputs.items()
                if spin.value() > 0]