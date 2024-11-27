import os
import time
import requests
import zipfile
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QProgressBar, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal


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


# Основное окно приложения
class DownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Загрузка архива")
        self.resize(400, 100)

        self.progress_bar = QProgressBar(self)
        self.label = QLabel("Прогресс: 0% Скорость: 0 МБ/с Оставшееся время: Неизвестно", self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.download_url = "https://nextcloud.492x9ud43mz9xi49xm342sda.com/index.php/s/gTHbCY69fRi5p4W/download"
        self.file_path = "progs.zip"
        self.total_size = 1_020_000_000  # 1 ГБ (размер известен заранее)

        self.thread = DownloadThread(self.download_url, self.file_path, self.total_size)
        self.thread.progress.connect(self.update_progress)
        self.thread.speed.connect(self.update_speed)
        self.thread.time_left.connect(self.update_time_left)
        self.thread.finished.connect(self.download_finished)
        self.thread.start()

    def update_progress(self, percent):
        self.progress_bar.setValue(percent)

    def update_speed(self, speed):
        self.speed = speed

    def update_time_left(self, time_left):
        self.label.setText(f"Прогресс: {self.progress_bar.value()}% Скорость: {self.speed:.2f} МБ/с Оставшееся время: {time_left:.2f} мин.")






    def download_finished(self):
        self.label.setText("Скачивание завершено. Распаковка архива...")
        self.extract_archive()
        self.move_folders()
        self.label.setText("Завершено.")
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


if __name__ == "__main__":
    app = QApplication([])
    window = DownloaderApp()
    window.show()
    app.exec_()
