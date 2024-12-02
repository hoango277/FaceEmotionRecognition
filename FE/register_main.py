import json
import requests
from PyQt5 import QtWidgets
from register import Ui_RegisterDialog
from login_main import LoginWindow


class RegisterWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_RegisterDialog()
        self.ui.setupUi(self)

        self.ui.registerConfirmButton.clicked.connect(self.handle_register)
        self.ui.alreadyHaveAccountLabel.linkActivated.connect(self.show_login)

    def handle_register(self):
        first_name = self.ui.firstNameInput.text()
        last_name = self.ui.lastNameInput.text()
        username = self.ui.registerUsernameInput.text()
        email = self.ui.emailInput.text()
        password = self.ui.registerPasswordInput.text()
        confirm_password = self.ui.confirmPasswordInput.text()

        if password != confirm_password:
            self.show_error_message("Password and confirm password do not match!")
            return

        if not first_name or not last_name or not username or not email or not password:
            self.show_error_message("Vui lòng điền đầy đủ thông tin.")
            return

        url = "http://127.0.0.1:8000/api/auth/register"
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "password": password
        }

        response = requests.post(url, json=data)
        try:
            response_data = response.json()
            message = response_data.get("message", "")

            if message == "Register successful!":
                self.show_success_message("Đăng ký thành công!")
            else:
                self.show_error_message(f"{message}")
        except Exception as e:
            self.show_error_message(f"Lỗi trong quá trình đăng ký: {str(e)}")

    def show_success_message(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Thông báo")
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.buttonClicked.connect(self.on_success_message_click)

        msg.exec_()

    def on_success_message_click(self, button):

        self.login_window = LoginWindow()
        self.login_window.show()
        self.hide()

    def show_error_message(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Lỗi")
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def show_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.hide()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    register_window = RegisterWindow()
    register_window.show()
    sys.exit(app.exec_())
