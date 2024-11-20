from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget

import sys



def application():
    app = QApplication(sys.argv)
    window = QMainWindow()

    window.setWindowTitle("First Installer")
    window.setGeometry(600, 300, 300, 300)

    text = QtWidgets.QLabel(window)
    text.setText("Первичная установка!!!!")

    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    application()