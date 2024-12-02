import sys
import requests
from PyQt5 import QtWidgets
from forgot_password import ForgotPasswordDialog
from login_main import LoginWindow  # Đảm bảo bạn đã có LoginWindow ở đây


class ForgotPasswordWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = ForgotPasswordDialog()  # Khởi tạo đối tượng ForgotPasswordDialog
        self.ui.setupUi(self)  # Gọi phương thức setupUi để thiết lập giao diện

        # Kết nối sự kiện "confirmButton"
        self.ui.confirmButton.clicked.connect(self.handle_confirm)

        # Sử dụng mousePressEvent cho QLabel để bắt sự kiện nhấn chuột
        self.ui.backLabel.mousePressEvent = self.show_login  # Thay thế clicked bằng mousePressEvent

    def handle_confirm(self):
        email = self.ui.emailInput.text()

        if not email:
            QtWidgets.QMessageBox.warning(self, "Thông báo", "Vui lòng nhập email!")
            return

        # API URL của bạn (đảm bảo đã chạy API ở localhost)
        api_url = "http://127.0.0.1:8000/api/email"
        payload = {
            "email": email,
        }

        try:
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Thành công",
                                                  "Yêu cầu quên mật khẩu thành công. Vui lòng kiểm tra email của bạn!")
            else:
                QtWidgets.QMessageBox.warning(self, "Thất bại", f"Lỗi từ server: {response.text}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Lỗi kết nối", f"Không thể kết nối đến server. Chi tiết lỗi: {str(e)}")

    def show_login(self, event):
        # Chuyển sang cửa sổ login
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()  # Đóng cửa sổ quên mật khẩu khi quay lại login


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ForgotPasswordWindow()  # Khởi tạo cửa sổ quên mật khẩu
    window.show()  # Hiển thị cửa sổ quên mật khẩu
    sys.exit(app.exec_())
