import json
import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from login import Ui_LoginWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        self.ui.loginButton.clicked.connect(self.handle_login)
        self.ui.registerButton.clicked.connect(self.show_register)
        self.ui.forgotPasswordLabel.mousePressEvent = self.show_forgot_password

    def handle_login(self):
        username = self.ui.usernameInput.text()
        password = self.ui.passwordInput.text()
        if not username or not password:
            self.show_error_message("Vui lòng nhập tên người dùng và mật khẩu.")
            return

        url = "http://127.0.0.1:8000/api/auth/login"
        data = {"username": username, "password": password}

        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                json_response = response.json()
                access_token = json_response.get('access_token')
                token_type = json_response.get('token_type')
                if access_token and token_type:
                    self.save_token(access_token, token_type)
                    self.show_home()
                else:
                    self.show_error_message("Thông tin đăng nhập không hợp lệ.")
            else:
                self.show_error_message("Tên người dùng hoặc mật khẩu không chính xác.")
        except requests.exceptions.RequestException as e:
            self.show_error_message(f"Lỗi kết nối: {str(e)}")

    def handle_send_code(self, forgot_password_window):
        email = forgot_password_window.ui.emailInput.text()

        if not email:
            self.show_error_message("Vui lòng nhập email!")
            return

        url = "http://127.0.0.1:8000/api/email"
        payload = {"email": email}

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Thành công", "Mã xác nhận đã được gửi đến email của bạn.")
            else:
                self.show_error_message(f"Không thể gửi mã xác nhận. Lỗi: {response.text}")
        except requests.exceptions.RequestException as e:
            self.show_error_message(f"Lỗi kết nối: {str(e)}")

    def handle_reset_password(self, email):
        url = "http://127.0.0.1:8000/api/reset"
        payload = {"email": email}

        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Thành công", "Mật khẩu đã được đặt lại.")
            else:
                self.show_error_message(f"Không thể đặt lại mật khẩu. Lỗi từ server: {response.text}")
        except requests.exceptions.RequestException as e:
            self.show_error_message(f"Lỗi kết nối: {str(e)}")

    def start_camera(self):
        token = self.load_token()
        if not token:
            self.show_error_message("Cần phải đăng nhập trước khi bật camera.")
            return

        url = "http://127.0.0.1:8000/api/stream"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Thành công", "Kết nối đến camera thành công!")
            else:
                self.show_error_message(f"Lỗi kết nối camera: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.show_error_message(f"Lỗi kết nối: {str(e)}")

    def load_token(self):
        try:
            with open("token.json", "r") as token_file:
                token_data = json.load(token_file)
                return token_data.get("access_token")
        except Exception as e:
            return None

    def show_forgot_password(self, event):
        from forgot_password_main import ForgotPasswordWindow
        self.forgotPasswordWindow = ForgotPasswordWindow()

        self.ui.forgotPasswordLabel.mousePressEvent = self.show_forgot_password
        self.forgotPasswordWindow.show()
        self.hide()

    def show_error_message(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Lỗi")
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def save_token(self, access_token, token_type):
        token_data = {"access_token": access_token, "token_type": token_type}
        try:
            with open("token.json", "w") as token_file:
                json.dump(token_data, token_file)
        except Exception as e:
            print(f"Không thể lưu token: {str(e)}")

    def show_home(self):
        from home_main import HomeWindow
        self.homeWindow = HomeWindow()
        self.homeWindow.show()
        self.hide()

    def show_register(self):
        from register_main import RegisterWindow
        self.registerWindow = RegisterWindow()
        self.registerWindow.show()
        self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
