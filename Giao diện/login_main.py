import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from PyQt5 import QtWidgets
from login import Ui_MainWindow  # Import giao diện từ file login.py
from camera import Ui_CameraWindow  # Import giao diện từ file camera.py
from register import Ui_RegisterDialog  # Import giao diện từ file register.py
import requests

class MainApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loginButton.clicked.connect(self.login_user)
        self.registerButton.clicked.connect(self.open_register_window)  # Chuyển sang giao diện đăng ký khi nhấn nút

    def login_user(self):
        url = 'http://127.0.0.1:8000/login'
        data = {
            "username": self.usernameInput.text(),
            "password": self.passwordInput.text()
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            message = response.json().get("message")
            if message == "Login successful":
                self.show_popup("Thông báo", "Đăng nhập thành công!")
                self.open_camera_window()  # Mở cửa sổ camera khi đăng nhập thành công
            else:
                self.show_popup("Thông báo", "Đăng nhập thất bại: " + message)
        else:
            self.show_popup("Thông báo", "Có lỗi xảy ra!")

    def show_popup(self, title, message):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def open_camera_window(self):
        # Tạo một cửa sổ mới cho Camera
        self.camera_window = QtWidgets.QMainWindow()
        self.ui = Ui_CameraWindow()
        self.ui.setupUi(self.camera_window)
        self.camera_window.show()
        # Ẩn cửa sổ đăng nhập
        self.hide()

    def open_register_window(self):
        # Tạo một cửa sổ mới cho Đăng ký
        self.register_window = QDialog()
        self.ui = Ui_RegisterDialog()
        self.ui.setupUi(self.register_window)
        self.register_window.show()
        # Ẩn cửa sổ đăng nhập
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
