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
        self.accepted = False
        self.setWindowTitle("Авторизация")
        self.ui.input_but.clicked.connect(self.handle_login)

    def handle_login(self):
        #проверка логина и пароля
        #   if self.ui.log_input.text() == "admin" and self.ui.pass_input.text() == "123":
        #       self.accepted = True
        #       self.close()
        #   else:
        #       QtWidgets.QMessageBox.warning(self, "ERROR", "Неверный логин или пароль")
        
        self.accepted = True
        self.close()

#главный экран

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

    login = LoginWindow()
    login.show()

    #цикл только на login окне
    app.exec_()

    if login.accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()