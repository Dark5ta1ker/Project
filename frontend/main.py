import sys
from PyQt5 import QtWidgets
from MainWindow import Ui_MainWindow
from input_gos import Ui_MainWindow as Ui_LoginWindow

# Окно авторизации
class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.accepted = False  # Флаг успешной авторизации
        self.setWindowTitle("Авторизация")
        self.ui.input_but.clicked.connect(self.handle_login)

    def handle_login(self):
        # Проверка логина и пароля
        if self.ui.log_input.text() == "admin" and self.ui.pass_input.text() == "123":
            self.accepted = True
            self.close()  # Закрываем окно авторизации
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def closeEvent(self, event):
        # Если окно закрывается, а авторизация не пройдена, завершаем приложение
        if not self.accepted:
            sys.exit(0)
        event.accept()

# Главное окно
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Система управления отелем")
        self.showMaximized()

def main():
    app = QtWidgets.QApplication(sys.argv)

    # Отображаем окно авторизации
    login = LoginWindow()
    login.show()

    # Запускаем цикл событий
    app.exec_()

    # Если авторизация успешна, открываем главное окно
    if login.accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()