from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget

import sys


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # Установка заголовка
        self.setWindowTitle("First Installer")
        # Установка размеров окна (xy где появляется, xy размеры)
        self.setGeometry(600, 300, 300, 300)


        # Создание текствого виджета
        self.text = QtWidgets.QLabel(self)
        self.text.setText("Первичная установка")
        self.text.move(100, 0)
        self.text.setFixedWidth(150)


        # Создание кнопки
        self.button = QtWidgets.QPushButton(self)
        self.button.move(100, 150)
        self.button.setText("Start")
        self.button.setFixedWidth(100)
        self.button.clicked.connect(self.button_click)


        # Объявляем переменную и новый лейбл
        self.response = QtWidgets.QLabel(self)


    # Ответ в приложении на нажатие кнопки
    def button_click(self):
        self.response.setText("Скрипт начал работу")
        self.response.move(95, 180)
        self.response.setFixedWidth(150)
        self.response.adjustSize()


def application():
    # Создание объекта app (экземпляр класса QApplication)
    # Параметр sys.argv это список аргументов командной строки
    app = QApplication(sys.argv)
    # Создаем экземпляр собственного класса
    window = Window()
    # Метод show показывает текст
    window.show()
    # Указание «запустить приложение, пока пользователь не закроет его»
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()