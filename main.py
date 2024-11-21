from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from backQt import Backendlogic
from frontQt import Ui_MainWindow

import sys
import subprocess


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Экземпляр логики
        self.logic = Backendlogic()

        # Подключение кнопки к обработчику
        self.ui.pushButton.clicked.connect(self.handle_button_click)

    # Ответ в приложении на нажатие кнопки
    def handle_button_click(self):
        # Вызов логики из backend
        result = self.logic.process_button_action()

        # Показ messageBox с сообщением
        msg = QMessageBox(self)
        msg.setWindowTitle("Предупреждение")
        msg.setText(result)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        subprocess.run(["C:\\Users\SysAlex\PycharmProjects\First_Installer\download.exe"])


if __name__ == "__main__":
    # Создание объекта app (экземпляр класса QApplication)
    # Параметр sys.argv это список аргументов командной строки
    app = QApplication(sys.argv)
    # Создаем экземпляр собственного класса
    window = Window()
    # Метод show показывает текст
    window.show()
    # Указание «запустить приложение, пока пользователь не закроет его»
    sys.exit(app.exec_())