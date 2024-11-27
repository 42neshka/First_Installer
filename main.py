from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from backQt import Backendlogic
from frontQt import Ui_MainWindow
from PyQt5.QtCore import QThread, pyqtSignal
import requests
import time
import os
import shutil
import zipfile


import sys
import subprocess

# Основное окно
class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # ui = экземпляр класса из frontQt Ui_MainWindow
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Экземпляр логики
        self.logic = Backendlogic()

        # Подключение кнопки к обработчику
        self.ui.pushButton.clicked.connect(self.handle_button_click)

        self.download_url = "https://nextcloud.492x9ud43mz9xi49xm342sda.com/index.php/s/gTHbCY69fRi5p4W/download"
        self.file_path = "progs.zip"
        self.total_size = 1_020_000_000  # 1 ГБ (размер известен заранее)









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
        #
        # subprocess.run(["C:\\Users\SysAlex\PycharmProjects\First_Installer\download.exe"])

        # Создаем экземпляр класса с параметрами
        self.thread = DownloadThread(self.download_url, self.file_path, self.total_size)
        self.thread.progress.connect(self.update_progress)
        self.thread.speed.connect(self.update_speed)
        self.thread.time_left.connect(self.update_time_left)
        self.thread.finished.connect(self.download_finished)
        self.thread.start()



    def update_progress(self, percent):
        self.ui.progressBar.setValue(percent)

    def update_speed(self, speed):
        self.ui.speed = speed

    def update_time_left(self, time_left):
        self.ui.labelDownload.setText(
            f"Прогресс: {self.ui.progressBar.value()}% Скорость: {getattr(self, 'speed', 0):.2f} МБ/с Оставшееся время: {time_left:.2f} мин."
        )

    def download_finished(self):
        self.label.setText("Скачивание завершено. Распаковка архива...")
        self.extract_archive()
        self.move_folders()
        self.ui.labelDownload.setText("Завершено")
        time.sleep(2)
        self.close()

    def extract_archive(self):
        with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
            zip_ref.extractall(".")

    def move_folders(self):
        documents_path = os.path.expanduser("~/Documents")
        folders_to_move = {
            "./progs/obs_profile": documents_path,
            # "./progs/PP Friendly": documents_path,
            "./progs/RebootRestoreRx3": documents_path,
        }

        for source, destination in folders_to_move.items():
            if os.path.exists(source):
                folder_name = os.path.basename(source)
                final_destination = os.path.join(destination, folder_name)

                if os.path.exists(final_destination):
                    shutil.rmtree(final_destination)

                shutil.move(source, final_destination)



# Поток для скачивания файла
class DownloadThread(QThread):
    progress = pyqtSignal(int)
    speed = pyqtSignal(float)
    time_left = pyqtSignal(float)
    finished = pyqtSignal()

    def __init__(self, url, dest, total_size):
        super().__init__()
        self.url = url
        self.dest = dest
        self.total_size = total_size

    def run(self):
        with requests.get(self.url, stream=True) as response:
            response.raise_for_status()
            with open(self.dest, 'wb') as file:
                downloaded = 0
                start_time = time.time()

                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)

                        # Рассчитываем прогресс
                        percent = int((downloaded / self.total_size) * 100)
                        elapsed_time = time.time() - start_time
                        speed = downloaded / elapsed_time  # байт/сек
                        time_left = (self.total_size - downloaded) / speed if speed > 0 else 0

                        self.progress.emit(percent)
                        self.speed.emit(speed / 1_048_576)  # в МБ/с
                        self.time_left.emit(time_left / 60)  # в минутах

        self.finished.emit()




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