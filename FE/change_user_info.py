import json
import requests
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_EditUserInfoWindow(QtWidgets.QMainWindow):
    def __init__(self, user_info):
        super().__init__()
        self.user_info_window = user_info
    def setupUi(self):
        self.setObjectName("EditUserInfoWindow")
        self.resize(400, 350)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("background-color: #ECF0F1;")

        # Tạo các trường nhập liệu
        self.email_label = QtWidgets.QLabel("Email:", self.centralwidget)
        self.email_label.setGeometry(QtCore.QRect(50, 40, 120, 30))
        self.email_label.setStyleSheet("font-size: 14px; color: #34495E;")

        self.email_input = QtWidgets.QLineEdit(self.centralwidget)
        self.email_input.setGeometry(QtCore.QRect(180, 40, 200, 30))
        self.email_input.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #BDC3C7;
        """)

        self.first_name_label = QtWidgets.QLabel("Họ:", self.centralwidget)
        self.first_name_label.setGeometry(QtCore.QRect(50, 100, 120, 30))
        self.first_name_label.setStyleSheet("font-size: 14px; color: #34495E;")

        self.first_name_input = QtWidgets.QLineEdit(self.centralwidget)
        self.first_name_input.setGeometry(QtCore.QRect(180, 100, 200, 30))
        self.first_name_input.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #BDC3C7;
        """)

        self.last_name_label = QtWidgets.QLabel("Tên:", self.centralwidget)
        self.last_name_label.setGeometry(QtCore.QRect(50, 160, 120, 30))
        self.last_name_label.setStyleSheet("font-size: 14px; color: #34495E;")

        self.last_name_input = QtWidgets.QLineEdit(self.centralwidget)
        self.last_name_input.setGeometry(QtCore.QRect(180, 160, 200, 30))
        self.last_name_input.setStyleSheet("""
            font-size: 14px;
            padding: 5px;
            border-radius: 5px;
            border: 1px solid #BDC3C7;
        """)

        # Nút Xác nhận
        self.confirm_button = QtWidgets.QPushButton("Xác nhận", self.centralwidget)
        self.confirm_button.setGeometry(QtCore.QRect(50, 220, 150, 40))
        self.confirm_button.setStyleSheet("""
            background-color: #3498DB;
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 20px;
            padding: 10px;
        """)

        # Nút Hủy
        self.cancel_button = QtWidgets.QPushButton("Hủy", self.centralwidget)
        self.cancel_button.setGeometry(QtCore.QRect(230, 220, 150, 40))
        self.cancel_button.setStyleSheet("""
                    background-color: #E74C3C;
                    color: white;
                    font-size: 16px;
                    border: none;
                    border-radius: 20px;
                    padding: 10px;
                """)


        # Kết nối các nút với hành động
        self.confirm_button.clicked.connect(self.update_user_info)
        self.cancel_button.clicked.connect(self.cancel)

        self.setCentralWidget(self.centralwidget)

    def cancel(self):
        try:
            self.user_info_window.show()  # Hiển thị lại cửa sổ UserInfoWindow
            self.close()  # Đóng cửa sổ thay đổi mật khẩu
        except Exception as e:
            print(e)

    def get_token_from_file(self):
        """ Đọc token từ file token.json """
        try:
            with open('token.json', 'r') as f:
                data = json.load(f)
                return data.get('access_token')
        except FileNotFoundError:
            print("File token.json không tồn tại!")
            return None

    def update_user_info(self):
        email = self.email_input.text()
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()

        # Kiểm tra nếu các trường không trống
        if not email or not first_name or not last_name:
            QtWidgets.QMessageBox.warning(None, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Gửi yêu cầu để cập nhật thông tin người dùng qua API
        url = "http://127.0.0.1:8000/api/users/info"
        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
        }
        token = self.get_token_from_file()

        if not token:
            QtWidgets.QMessageBox.warning(None, "Lỗi", "Không có token để xác thực!")
            return

        headers = {
            'Authorization': f'Bearer {token}'
        }

        # Gửi yêu cầu PUT đến API
        response = requests.put(url, headers=headers, json=data)

        if response.status_code == 200:
            try:
                response_data = response.json()
                message = response_data.get("message", "")

                # Kiểm tra xem phản hồi có chứa thông điệp thành công không
                if message == "User info changed":
                    QtWidgets.QMessageBox.information(None, "Thành công", "Cập nhật thông tin thành công!")
                else:
                    # Nếu không có thông điệp như mong đợi
                    QtWidgets.QMessageBox.warning(None, "Lỗi", f"{message}")
            except ValueError:
                QtWidgets.QMessageBox.warning(None, "Lỗi", "Không thể đọc dữ liệu JSON từ API!")
        else:
            QtWidgets.QMessageBox.warning(None, "Lỗi",
                                          f"Không thể cập nhật thông tin: {response.status_code} - {response.text}")



