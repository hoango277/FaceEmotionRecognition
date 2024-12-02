
import requests

import sys

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer, Qt, QUrl
from camera import Ui_CameraWindow
from home_main import HomeWindow


class CameraWindow(QMainWindow, Ui_CameraWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.stream_url = 'http://127.0.0.1:8000/api/stream'  #

        self.timer = QTimer(self)

        # Kết nối các nút
        self.startButton.clicked.connect(self.start_camera)
        self.stopButton.clicked.connect(self.stop_camera)
        self.exitButton.clicked.connect(self.exit_camera)

    def start_camera(self):
        """Bắt đầu stream video từ API và hiển thị lên PyQt"""
        self.webview.setUrl(QUrl(self.stream_url))  # Gọi URL để bắt đầu stream
        self.webview.setVisible(True)  # Hiển thị QWebEngineView khi stream bắt đầu
        self.startButton.setEnabled(False)


    def stop_camera(self):
        """Dừng camera hoặc video stream"""
        api_url = "http://127.0.0.1:8000/api/stop"
        self.webview.setVisible(False)

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                self.timer.stop()
                QMessageBox.information(self, "Thành công", "Camera đã được dừng!")
            else:
                QMessageBox.warning(self, "Lỗi", f"Lỗi từ server: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể kết nối đến server: {e}")

    def exit_camera(self):
        """Dừng camera và đóng cửa sổ"""
        self.timer.stop()
        self.close()

        self.home_window = HomeWindow()
        self.home_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraWindow()
    window.show()
    sys.exit(app.exec_())
