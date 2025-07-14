import sys
from PyQt5 import QtWidgets
from MainWindow import Ui_MainWindow  # Импортируем класс главного окна
from input_gos import Ui_MainWindow as Ui_LoginWindow  # Импортируем класс окна авторизации

# Окно авторизации
class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Конструктор окна авторизации.
        """
        super().__init__()  # Вызываем конструктор родительского класса
        self.ui = Ui_LoginWindow()  # Создаем экземпляр интерфейса авторизации
        self.ui.setupUi(self)  # Настройка интерфейса
        self.accepted = False  # Флаг успешной авторизации (по умолчанию False)
        self.setWindowTitle("Авторизация")  # Устанавливаем заголовок окна
        self.ui.input_but.clicked.connect(self.handle_login)  # Привязываем обработчик к кнопке входа

    def handle_login(self):
        """
        Обработка нажатия на кнопку "Войти".
        Проверяет логин и пароль.
        """
        # Проверяем, совпадают ли введенные данные с заданными значениями
        if self.ui.log_input.text() == "admin" and self.ui.pass_input.text() == "123":
            self.accepted = True  # Устанавливаем флаг успешной авторизации
            self.close()  # Закрываем окно авторизации
        else:
            # Если данные неверны, показываем предупреждение
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")

    def closeEvent(self, event):
        """
        Обработка события закрытия окна.
        Если авторизация не пройдена, завершаем приложение.
        """
        if not self.accepted:  # Если авторизация не была успешной
            sys.exit(0)  # Завершаем приложение
        event.accept()  # Разрешаем закрытие окна

# Главное окно
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """
        Конструктор главного окна приложения.
        """
        super().__init__()  # Вызываем конструктор родительского класса
        self.ui = Ui_MainWindow()  # Создаем экземпляр интерфейса главного окна
        self.ui.setupUi(self)  # Настройка интерфейса
        self.setWindowTitle("Система управления отелем")  # Устанавливаем заголовок окна
        self.showMaximized()  # Открываем окно в полноэкранном режиме

def main():
    """
    Точка входа в приложение.
    """
    app = QtWidgets.QApplication(sys.argv)  # Создаем экземпляр приложения PyQt

    # Отображаем окно авторизации
    login = LoginWindow()  # Создаем экземпляр окна авторизации
    login.show()  # Показываем окно авторизации

    # Запускаем цикл событий приложения
    app.exec_()

    # Если авторизация успешна, открываем главное окно
    if login.accepted:  # Проверяем флаг успешной авторизации
        main_window = MainWindow()  # Создаем экземпляр главного окна
        main_window.show()  # Показываем главное окно
        sys.exit(app.exec_())  # Запускаем новый цикл событий для главного окна

if __name__ == "__main__":
    main()  # Вызываем функцию main()